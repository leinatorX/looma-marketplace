# 图像提示词模板与模型写法

## 使用场景

需要为 AI 视频参考资产撰写图像提示词时使用本文件：定妆照、角色三视图、道具/产品图、场景参考图、风格帧、首尾帧、封面图。默认输出提示词本身，不重复做资产规划（资产规划见 `video-asset-art`）。

## 通用提示词骨架

任何类型图先按此顺序装填信息，再套用对应模板：

```text
用途：这张图在成片/流程中干什么。
主体：谁/什么出现，稳定特征（脸、服装、材质、标识）。
构图：景别、主体位置、角度、背景。
风格：写实/电影感/广告摄影/产品摄影/赛博/复古/动画。
光线与影调：光线方向、色温、影调。
画幅：1:1 / 3:4 / 9:16 / 16:9。
限制：禁止变化项与避免项（裁切、变形、乱码、多余人物）。
```

## 六类资产模板

### 1. 定妆照

```text
用途：AI 视频主角定妆照，用于后续图生视频和角色一致性参考。
主体：{角色身份、年龄、体型、脸部特征、发型、肤色、气质}。
服装：{服装款式、颜色、材质、配饰、关键标识}。
姿态：全身正面站立，自然站姿，双手自然下垂，表情基准为 {表情}。
背景：干净中性背景，不遮挡主体。
风格：{写实/电影感/广告摄影/角色设定图/产品摄影}。
画幅：{1:1 / 3:4 / 9:16 / 16:9}。
限制：保持完整身体，避免裁切，避免多人物，避免文字乱码，避免脸部变形。
```

### 2. 角色三视图或多角度图

```text
用途：多镜头反复出现的角色多角度参考，锁定正/侧/背一致性。
主体：{角色身份、年龄、体型、脸部特征、发型、肤色、气质}。
服装：{服装款式、颜色、材质、配饰、关键标识}。
角度：同一角色正面、侧面、背面三视图，比例与细节完全一致。
姿态：三视图均自然站立，表情基准为 {表情}。
背景：干净中性背景，三视图使用同一背景色。
风格：{角色设定图/写实/电影感}。
画幅：{1:1 / 3:4}。
限制：同一张图内三个角度必须保持同一角色设计，避免体积/脸型漂移。
```

### 3. 道具/产品图

```text
用途：{产品广告/设备演示/事故道具/关键线索} 参考图。
主体：{产品/道具名称与关键细节}。
视图：{干净背景版 / 使用场景版}，两者都需要时各出一张。
构图：{居中/微侧/特写细节}，产品主体占画面 {60-80%}。
光线：{棚拍柔光/自然光/影棚主光+轮廓光}。
风格：{产品摄影/广告摄影/写实}。
画幅：{1:1 / 3:4 / 16:9}。
限制：保持品牌标识原样，避免多角度混排，避免文字乱码，避免比例变形。
```

### 4. 场景参考图

```text
用途：AI 视频主场景参考图，用于统一后续镜头的空间、光线和美术方向。
场景：{地点、时代、天气、时间、空间结构}。
视觉元素：{建筑、道路、家具、设备、环境道具、标识物}。
光线：{自然光/霓虹/阴天/夜景/强背光/低调光}。
风格：{写实电影感/纪录片/广告片/灾难片/复古胶片}。
构图：{广角/远景/中景/对称/引导线/俯拍/低角度}。
画幅：{16:9 / 9:16 / 1:1}。
限制：不要出现主角，避免无关文字，避免风格漂移。
```

### 5. 风格帧

```text
用途：锁定全片色彩、影调、摄影质感和画质的方向帧（可不进正片）。
画面主题：{与全片一致的场景/物件/氛围代表画面}。
风格核心：{写实/胶片/纪录片/赛博/复古/动画/广告片}。
色彩影调：{主色调、饱和度、对比度、色温}。
摄影质感：{胶片颗粒/锐度/景深/镜头感}。
光线：{光线方向与性质}。
画幅：{16:9 / 9:16 / 1:1}。
限制：本帧只定风格，不引入需要保持一致性的具体角色。
```

### 6. 首尾帧

```text
序列编号：{Q01}
用途：为 {视频模型} 生成首尾帧参考。

首帧：
{主体} 位于 {场景}，处于 {动作起点}。构图为 {景别、主体位置、镜头角度}，光线和风格保持 {风格}。

尾帧：
同一主体、同一服装、同一场景和同一摄影风格。主体完成 {动作结果}，位置变化为 {空间变化}，构图与首帧可自然衔接。

连续性限制：
保持同一角色外观、同一环境结构、同一光线方向，不要改变服装、脸、道具和镜头轴线。
```

## 序列生成方式与提示词重点

| 生成方式 | 适合镜头 | 提示词重点 |
| --- | --- | --- |
| 文生视频 | 空镜、环境、低一致性要求 | 完整描述主体、动作、场景、镜头和风格 |
| 图生视频 | 角色、产品、品牌一致性重要 | 写清参考图保持项和运动项 |
| 首帧视频 | 必须从指定构图开始 | 首帧锁定构图和主体，视频提示词只写运动与镜头变化 |
| 首尾帧视频 | 动作起止都重要、转场精准 | 描述首尾帧关系，避免中途复杂动作过多 |
| 多参考图视频 | 同时锁定人物/道具/场景/风格 | 每张参考图标注用途，避免模型混用 |
| 局部编辑后视频 | 只改某个区域 | 先用图像编辑修好参考图，再进入视频生成 |

## GPT Image 2 写法

官方资料要点：

- `gpt-image-2` 是 OpenAI 的图像生成和编辑模型，支持文本和图像输入，输出图像。
- OpenAI 图像生成指南说明，Image API 可生成图像、编辑图像，也可以用一张或多张图作为参考生成新图。
- `gpt-image-2` 会以高保真方式处理图像输入，相关保真参数无需手动调整。
- 可设置尺寸、质量、格式、压缩等输出参数。
- 官方限制包括复杂提示可能较慢、精确文字仍可能出错、跨多次生成的一致性可能不稳定、精确构图仍可能困难。

提示词结构：

```text
Generate a {aspect ratio} image for AI video reference.
Purpose: {character look / scene reference / prop reference / first frame / last frame}.
Subject: {clear subject and stable identifiers}.
Composition: {shot size, angle, subject position, background}.
Details to preserve: {face, clothing, logo, material, prop, color}.
Style and lighting: {photorealistic, cinematic, product photography, lighting}.
Output use: this image will be used as {image-to-video reference / start frame / end frame}.
Constraints: avoid {cropping, distorted face, unreadable text, extra characters, inconsistent logo}.
```

适合：定妆照、产品图、道具图、场景图；多图参考组合；局部编辑（换服装、移除背景、修正道具、生成透明背景素材）。

## Nano Banana Pro 写法

官方资料要点：

- Google 官方将 Nano Banana Pro 对应到 Gemini 3 Pro Image，面向专业资产生产、复杂指令和高保真文字渲染。
- Gemini API 图像生成支持文本、图像或组合输入，并支持对图像进行编辑和多轮迭代。
- Google 官方提示词建议包含主体、构图、动作、地点、风格；进一步细化相机角度、光线、画幅、文字集成和事实约束。
- 官方提示词文章提到不同产品表面对可输入图像数量的支持可能不同，最多可到 14 张图，需按具体平台确认。
- 官方仍提醒文字、事实准确性、复杂编辑、图像融合和角色一致性可能需要人工复核。

提示词结构：

```text
Create a {aspect ratio} professional AI video reference image.
Story purpose: {why this asset is needed in the film}.
Subject: {who/what appears, exact visual identity}.
Composition: {close-up / wide shot / low angle / portrait / product layout}.
Action or pose: {standing, holding, turning, running, object open/closed}.
Location: {environment, time, weather, background}.
Style: {photorealistic, cinematic, film noir, product photography, diagram, poster}.
Camera and lighting: {lens feel, depth of field, lighting direction, color grade}.
Text requirements: {exact visible text, font, placement}; if text is not needed, say no text.
Reference usage: {which input image controls character / prop / scene / style}.
Constraints: preserve {identity, logo, costume, color}; avoid {extra people, artifacts, illegible text}.
```

适合：专业定妆照、角色多角度图、海报、信息图、带文字视觉、品牌视觉；多参考图融合；需要世界知识或事实约束的图表、示意图和科普视觉（必须人工复核事实）。

## 图生图/编辑场景

基于已有参考图修改时，在提示词中明确：

```text
原始参考：{输入图 A 锁定角色}/ {输入图 B 锁定场景}。
要改：{换服装/去背景/补细节/修正道具/统一风格}。
保持：{其他所有内容按输入图原样}。
避免：{引入新角色、改动脸型、改变光线方向}。
```

## 官方来源

- OpenAI GPT Image 2 model page: https://developers.openai.com/api/docs/models/gpt-image-2
- OpenAI Image generation guide: https://developers.openai.com/api/docs/guides/image-generation
- Google Gemini image generation guide: https://ai.google.dev/gemini-api/docs/image-generation
- Google Nano Banana Pro prompt tips: https://blog.google/products-and-platforms/products/gemini/prompting-tips-nano-banana-pro/
- Google Nano Banana Pro launch post: https://blog.google/innovation-and-ai/products/nano-banana-pro/
