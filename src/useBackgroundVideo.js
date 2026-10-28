import { useEffect, useRef, useState } from 'react';

// No scroll handler or animation loop: only react to visibility boundaries.
export function useBackgroundVideo(videoRef, blocked) {
  const [playing, setPlaying] = useState(false);
  const [staticOnly, setStaticOnly] = useState(false);
  const userPaused = useRef(false);
  const syncRef = useRef(() => {});

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    const connection = navigator.connection;
    let visible = false;
    let disposed = false;
    let idleId;
    let timerId;
    const constrained = () => reducedMotion.matches || Boolean(connection?.saveData);
    const cancelStart = () => {
      if (idleId !== undefined) window.cancelIdleCallback(idleId);
      clearTimeout(timerId);
      idleId = undefined;
      timerId = undefined;
    };
    const sync = () => {
      cancelStart();
      const useStatic = constrained();
      setStaticOnly(useStatic);
      if (useStatic || !visible || document.hidden || blocked || userPaused.current) {
        video.pause();
        // A CSS-hidden video must not continue downloading in reduced-motion mode.
        if (useStatic && video.hasAttribute('src')) {
          video.removeAttribute('src');
          video.load();
        }
        return;
      }
      if (document.readyState !== 'complete') return;
      const start = () => {
        if (disposed || !visible || document.hidden || blocked || userPaused.current || constrained()) return;
        if (!video.hasAttribute('src')) video.src = '/assets/hero.mp4';
        video.play().catch(() => setPlaying(false));
      };
      if (video.hasAttribute('src')) start();
      else if ('requestIdleCallback' in window) idleId = window.requestIdleCallback(start, { timeout: 1500 });
      else timerId = window.setTimeout(start, 250);
    };
    syncRef.current = sync;
    const observer = new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      sync();
    }, { threshold: 0 });
    observer.observe(video.closest('section'));
    document.addEventListener('visibilitychange', sync);
    window.addEventListener('load', sync);
    reducedMotion.addEventListener('change', sync);
    connection?.addEventListener('change', sync);
    sync();
    return () => {
      disposed = true;
      cancelStart();
      observer.disconnect();
      document.removeEventListener('visibilitychange', sync);
      window.removeEventListener('load', sync);
      reducedMotion.removeEventListener('change', sync);
      connection?.removeEventListener('change', sync);
      video.pause();
    };
  }, [videoRef, blocked]);

  const toggle = () => {
    userPaused.current = !videoRef.current.paused;
    syncRef.current();
  };
  return { playing, setPlaying, staticOnly, toggle };
}
