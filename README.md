# WF300 — 300 mm 双手晶圆夹取治具

Open hardware for a two-hand, edge-contact 300 mm wafer gripper.

**P1D1 工程试制设计 / Engineering prototype. 尚未完成实物资格验证，不能凭本仓库直接放行真实工艺晶圆使用。**

![Assembly geometry — schematic only](assets/assembly-isometric.svg)

本项目公开双手持握、水平低速转移晶圆的机械设计、尺寸图、BOM 和生产装配说明。它不是安全双手联锁，也不是 FOUP 取片器、吸盘或平桌铲片工具。

## 从哪里开始

1. 阅读 [安全边界与未关闭事项](SAFETY.md) 和 [公开版说明](docs/PUBLICATION.md)。
2. 查看 [12 页 A3 尺寸图](drawings/WF300-DH_P1D1_drawings.pdf) 与 [11 页生产装配说明](docs/WF300-DH_P1D1_assembly_manual.pdf)。
3. 下载 [闭合 FreeCAD 模型](cad/WF300-DH_P1D1_closed.FCStd)、[全开模型](cad/WF300-DH_P1D1_open.FCStd) 或 [闭合 STEP](cad/WF300-DH_P1D1_closed.step)。
4. 加工评审使用 [5 种自制件 STEP](parts_step)、[BOM](manufacturing/BOM_P1D1.csv)、[紧固连接记录](manufacturing/16个紧固连接与扭矩记录.csv) 和 [首件验收记录](manufacturing/首件验收记录.csv)。空白记录不代表合格。

## 设计边界

| 项目 | P1D1 基线 |
| --- | --- |
| 晶圆 | Ø300 mm；厚度 0.50–0.90 mm，参考片 0.775 mm |
| 接触 | 正反面最外缘 2 mm 内允许接触；四个未填充 PEEK 槽块 |
| 结构材料 | 6061-T651 框架、316L 导杆/端盖、A4-70 螺钉 |
| 采购件 | Ensinger TECAPEEK SX natural；igus JSM-1012-20；Lee Spring LP024K05S316；TE 31090 |
| 单侧行程 | 8 ± 0.20 mm，待首件检验 |
| 开启力目标 | 每手横向开启增量 2–5 N，峰值 ≤5 N；不含托举自重 |
| 洁净 / ESD 意图 | Class 100 左右 / ISO 5 操作区；金属独立接地、工位离子化；不是认证 |
| 使用假设 | 干态、水平、低速，20–25°C、40%–55% RH，无凝露、有防跌托盘 |

数值是需求、设计值或开发目标，不是实测合格结果。装配说明提供材料、表处、压装、线束、清洗、停点、检查及操作程序；任何代料或尺寸修改都需要重新验证。

## 文件组织

| 目录 | 内容 |
| --- | --- |
| `cad/` | 闭合 / 全开 FCStd 与 STEP，含简化采购件和参考晶圆 |
| `parts_step/` | 左右框架、槽块、导杆、端盖的局部坐标 STEP |
| `drawings/` | 12 页 PDF 及逐页 SVG / DXF |
| `manufacturing/` | 13 行 BOM、16 连接记录、首件验收表、公开来源链接 |
| `docs/` | 中文装配说明、版本范围与验证状态 |
| `tools/` | 无第三方依赖的只读文件校验工具，不是建模器或 CAM |
| `validation/` | 公开文件来源与哈希；不含内部详细测试记录 |

DXF 使用**纸面毫米**，标注由线、箭头和文字组成，不是关联式尺寸，不能直接当作 1:1 CAM。加工以经工程和工艺人员签署的关键二维尺寸、公差和要求为准，同版 STEP 补充复杂轮廓；矛盾需提偏差评审。

## 打开与校验

CAD 原件保留既有几何与对象结构。自制件为可编辑实体，不承诺完整草图约束或全参数生成历史。原生螺钉重算依赖 [FreeCAD Fasteners Workbench](https://github.com/shaise/FreeCAD_FastenersWB)，历史版本为 `79a06dc067b57ebc89532be835704eb2af5da96c`；没有该插件时，可使用 STEP 查看几何。

Python 3.10+，在仓库根目录运行：

```sh
python3 tools/verify_release.py
python3 -m unittest discover -s tests -v
```

这只检查发布文件、哈希、容器结构、BOM 数量及明显的本机路径/凭证模式，不会执行 CAD 内部 Python 对象，不会重算几何，也不会给制造、洁净、ESD 或晶圆安全放行。校验失败时退出码非零。

## 验证状态与贡献

装配说明引用了历史 CAD 检查结论；详细内部测试报告不属于本仓库的公开范围，因此不能仅凭本仓库独立复核这些历史结论。此次公开整理没有重跑依赖原工作环境的几何检查，也没有新增实片测试。详见 [验证状态](docs/VALIDATION.md)。

欢迎贡献制造可行性、人体工学、颗粒 / ESD 数据、减重设计和真正可重建的参数模型。请附版本、单位、假设、方法和原始证据，区分仿真与测量，见 [CONTRIBUTING](CONTRIBUTING.md)。

## 许可

项目权利范围内：硬件设计、图纸和 BOM 使用 **CERN-OHL-P-2.0**；独立软件使用 **MIT**；说明文档使用 **CC BY 4.0**。适用范围见 [LICENSING](LICENSING.md)，第三方工具和品牌见 [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES.md)。均不构成供应商背书或适用性保证。

---

### English summary

WF300 is an unqualified engineering prototype for two-hand, horizontal handling of 300 mm wafers, 0.50–0.90 mm thick, with permitted contact within the outer 2 mm of both faces. It includes native FreeCAD files, STEP models, dimensioned drawings, a BOM, and Chinese manufacturing/assembly instructions. Cleanliness, ESD, operating forces, damage risk, and service life remain unqualified. Read [SAFETY](SAFETY.md) before any physical trial. The portable verifier checks release integrity, not mechanical safety. Hardware: CERN-OHL-P-2.0; software: MIT; documentation: CC BY 4.0, subject to the scope and third-party notices above.
