# 职业方向探索与面试成长助手

当前项目已完成规格、唯一的 Spec Kit 技术计划、121 项任务及文档一致性修订。Phase 1 的 T001–T005 已建立 Django/Python 与浏览器测试脚手架；其余 116 项任务仍待实施，职业产品流程、应用数据模型与用户功能尚未实现。仓库中的主要资料：

- [功能规格](specs/001-career-interview-coach/spec.md)：首个可用版本的范围、行为和验收依据。
- [已批准的 Figma 原型索引](specs/001-career-interview-coach/prototype.md)：方向 2 的文件链接、关键画面及使用边界。
- [UX 补充说明](specs/001-career-interview-coach/ux-addendum.md)：简历文件导入与具体职位搜寻的流程、状态和交互。
- [规格检查表](specs/001-career-interview-coach/checklists/requirements.md)：规划前的规格就绪检查。
- [技术实施计划](specs/001-career-interview-coach/plan.md)：唯一的技术计划，包含需求映射、模块、实施顺序、测试、兼容性与风险。
- [实施任务](specs/001-career-interview-coach/tasks.md)：121 项任务及依赖、验证和审阅门槛；T001–T005 已完成，116 项待实施。
- [技术研究](specs/001-career-interview-coach/research.md)：技术选择、职位来源验证与尚待完成的上线验证。
- [数据模型](specs/001-career-interview-coach/data-model.md)：事实、版本、来源、冲突、复盘与保留规则。
- 接口契约：[应用 API](specs/001-career-interview-coach/contracts/application-api.md)、[外部服务](specs/001-career-interview-coach/contracts/external-services.md)、[交互与生命周期](specs/001-career-interview-coach/contracts/interaction-lifecycle.md)。
- [验证指南](specs/001-career-interview-coach/quickstart.md)：已验证的脚手架检查命令，以及后续应用验收场景。
- [Phase 1 设置证据](specs/001-career-interview-coach/evidence/setup.md)：依赖版本、离线边界、可运行命令与结果。

后续 agent 应先读规格、原型索引、上述 Spec Kit 计划及任务，只实施已获授权的范围，不另建竞争计划。原型展示交互与视觉设计；如与规格冲突，以规格为准，并记录需要确认的产品决策。Figma 画面复核、实际 AI/语音服务与部署保留策略验证仍需完成，不能把文档设计或测试替身当成上线验收证据。

基础配置的用途与当前边界：

- `.gitignore` 排除本地环境变量、虚拟环境、缓存、浏览器测试产物及根目录下的私有运行资料。真实简历、录音、数据库和导出应放入独立私有数据目录；不要放进源码、静态资源或测试样例。合成测试样例、迁移、依赖锁文件、`.agents` 和 `.specify` 仍可提交。
- `.editorconfig` 与 `.gitattributes` 统一 UTF-8、缩进和文本换行，并保留 Markdown 行末空格及二进制样例的内容。
- `.python-version` 和 `.nvmrc` 记录 Python 3.12 与 Node 24 系列；当前验证使用 Python 3.12.1、Node 24.14.0 和 npm 11.21.0。Python 运行时与开发依赖在 `requirements-dev.lock` 中带哈希锁定，Node 浏览器开发依赖由 `package-lock.json` 固定。
- `pyproject.toml` 配置 Ruff/mypy，`jsconfig.json` 配置 ES2022/checkJs/noEmit；当前只检查 Django 脚手架及测试代码，没有职业产品行为。`npm test` 运行类型检查、Node 浏览器规则测试和本机 Playwright 合成页面测试。
- `config/test_settings.py` 为自动化测试创建独立临时私有目录与进程内合成密钥，关闭外部服务，并拦截非回环 DNS/socket 请求。Playwright setup 测试只访问一次性本地 fixture origin，其他请求均被阻止。
- `.env.example` 提供无密钥的运行配置示例；现阶段没有 owner 绑定、产品服务或 provider 凭据。测试配置与开发默认值不能替代后续 owner 授权和 provider 验收。

尚未完成的内容包括应用数据模型/迁移、用户流程、owner provision、生产服务、后台任务、实际 AI/语音/职位来源、部署配置与人类验收。运行脚手架的命令见验证指南；后续命令均明确标为计划，不能视为已经通过的验收。
