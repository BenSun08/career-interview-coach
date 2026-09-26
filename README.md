# 职业方向探索与面试成长助手

当前项目已完成规格、Spec Kit 技术计划、121 项待实施任务及文档一致性修订，并添加基础仓库配置；尚无应用代码或可安装的依赖清单。仓库中的主要资料：

- [功能规格](specs/001-career-interview-coach/spec.md)：首个可用版本的范围、行为和验收依据。
- [已批准的 Figma 原型索引](specs/001-career-interview-coach/prototype.md)：方向 2 的文件链接、关键画面及使用边界。
- [UX 补充说明](specs/001-career-interview-coach/ux-addendum.md)：简历文件导入与具体职位搜寻的流程、状态和交互。
- [规格检查表](specs/001-career-interview-coach/checklists/requirements.md)：规划前的规格就绪检查。
- [技术实施计划](specs/001-career-interview-coach/plan.md)：唯一的技术计划，包含需求映射、模块、实施顺序、测试、兼容性与风险。
- [实施任务](specs/001-career-interview-coach/tasks.md)：121 项待实施任务及其依赖、验证和审阅门槛。
- [技术研究](specs/001-career-interview-coach/research.md)：技术选择、职位来源验证与尚待完成的上线验证。
- [数据模型](specs/001-career-interview-coach/data-model.md)：事实、版本、来源、冲突、复盘与保留规则。
- 接口契约：[应用 API](specs/001-career-interview-coach/contracts/application-api.md)、[外部服务](specs/001-career-interview-coach/contracts/external-services.md)、[交互与生命周期](specs/001-career-interview-coach/contracts/interaction-lifecycle.md)。
- [验证指南](specs/001-career-interview-coach/quickstart.md)：未来实施后的运行命令与验收场景，当前尚不可执行。

后续 agent 应先读规格、原型索引、上述 Spec Kit 计划及任务，获得相应授权后实施，不另建竞争计划。原型展示交互与视觉设计；如与规格冲突，以规格为准，并记录需要确认的产品决策。Figma 画面复核、实际 AI/语音服务与部署保留策略验证仍需完成，不能把文档设计或测试替身当成上线验收证据。

基础配置的用途与当前边界：

- `.gitignore` 排除本地环境变量、虚拟环境、缓存、浏览器测试产物及根目录下的私有运行资料。真实简历、录音、数据库和导出应放入独立私有数据目录；不要放进源码、静态资源或测试样例。合成测试样例、迁移、依赖锁文件、`.agents` 和 `.specify` 仍可提交。
- `.editorconfig` 与 `.gitattributes` 统一 UTF-8、缩进和文本换行，并保留 Markdown 行末空格及二进制样例的内容。
- `.python-version` 和 `.nvmrc` 分别记录计划的 Python 3.12 与 Node 24 系列；它们不安装运行时，也不锁定补丁版本。准确版本与依赖哈希随 T001/T003 验证后锁定。
- `pyproject.toml` 仅包含 Ruff 和 mypy 设置；`jsconfig.json` 为未来浏览器模块启用 ES2022、JSDoc/checkJs 与 noEmit。检查工具尚未安装，目标代码目录尚未创建，不能把这些文件当成可运行工具链。
- `.env.example` 是无密钥的开发配置约定草案，包含独立开发/测试数据目录、回环地址、待配置的 owner ID 和默认关闭的外部服务。当前没有设置读取器，复制为 `.env` 不会启动应用或落实安全控制；T001/W1 必须实现并验证解析、拒绝缺失凭据、owner 校验和离线网络限制。

本次配置准备不代表 T001–T005 完成。依赖清单和锁文件、Django 设置、Playwright 服务配置、CI 与部署配置仍随对应实施任务交付；运行和验收命令继续以验证指南中标明的未来命令为准。
