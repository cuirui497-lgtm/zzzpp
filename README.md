# 崔睿 · 个人作品集

基于 React 19 + Vite 6 的本地作品集基础版。最大版心 1700px，包含视频 Hero、个人介绍与四段工作经历、8 组精选项目、能力卡片和全屏联系页。

## 运行

```sh
npm install
npm run dev
```

本机尚未全局安装 Node.js，可直接双击 `启动预览.command`，使用 Codex 已提供的 Node.js 运行时启动。

```sh
npm run build
npm run preview
```

生产文件输出到 `dist/`，可部署到静态托管平台。

## 修改入口

- `src/main.jsx`：个人文案、工作经历、联系方式、页面结构。
- `src/projects.json`：项目名称、分类、简介及作品图顺序。
- `src/style.css`：颜色、排版、布局、响应式断点。
- `public/assets/hero.mp4`：6 秒无声循环背景，可直接替换同名文件。
- `public/assets/hero-poster.webp`：视频封面，低动态偏好时显示静态图。
- `public/assets/`：从提供的原始作品转换得到的 WebP；原始素材未修改。

`08` 为本次提供的项目目录数量，`04` 为简历中的工作经历数量；未编造业务增长数据。工作状态、所在地和联系方式按所提供简历整理。

项目支持分类、作品详情、Escape 关闭、焦点返回；联系方式支持邮箱、电话及微信复制。页面不依赖外部图片、字体或视频服务。

视频为首版专门制作的抽象环形动画。重新生成需要 Python、Pillow、numpy 和 imageio-ffmpeg，脚本位于 `scripts/generate-hero.py`；普通运行和构建无需这些依赖。

性能审查、优化前后资源对比与验证范围见 `PERFORMANCE.md`。视频可见性与节流策略位于 `src/useBackgroundVideo.js`。
