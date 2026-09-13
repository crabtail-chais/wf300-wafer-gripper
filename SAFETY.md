# 安全边界 / Safety and qualification status

**This is an unqualified engineering prototype, not a production-qualified wafer-handling device. CAD checks are not physical safety tests.**

截至 P1D1 发布基线，尚无实际首件测量、合格扭矩窗口、污染、晶圆损伤、ESD 或耐久验证结果。开源发布不改变工程准入状态。以下为工程警示和建议，不是在开源许可证之外增加用途限制。

## 制造与试验停点

- 图纸需由设计、加工、工艺和质量人员评审，尤其是表处后孔径、四点共面、PEEK 槽唇、端盖、有效螺纹和滑动配合。
- 0.08 / 0.20 / 0.15 N·m 是三类接头的试验起点，不是批准装配扭矩；需在同材料、表处和有效啮合条件下确定窗口。
- 弹簧、衬套和端子为简化几何，采购按准确料号和验收规范，不能制造这些包络体代替采购件。TE 端子实物接口和压接工艺仍需核验。
- 使用前须完成空载、假片厚度边界、偏载 / 单侧动作、力—行程、接头保持、颗粒、金属 / 离子污染及 ESD 检验。真实工艺片准入须现场责任人另行批准。
- 用防跌托盘及受控支撑进行试验；不得在悬空晶圆上调螺钉或拆弹簧。双手柄没有安全联锁功能。

## 不能从当前结果推导的结论

- 开启力 2–5 N/手不等于低自重或人体工学合格；持握载荷、疲劳、防滑、线束拖力需独立评估。
- Class 100 / ISO 5 是操作环境意图，未证明治具动态产尘符合要求。工艺污染限值仍需由实际使用方给定。
- 金属到公共点 ≤1 Ω、离子平衡与晶圆表面电位各 ±10 V 是开发目标。绝缘 PEEK / iglidur 不能单靠金属接地消电；离子器读数不等于晶圆读数；不承诺绝对 0 V。
- 合格接地路径需现场 ESD 负责人批准，不能短接人员腕带安全电阻。
- 100 / 1000 次是开发筛查节点，不是寿命额定值。
- 不覆盖热片、湿片、真空、竖直或冲击搬运、FOUP、平桌铲片与自动化设备联锁。

事故、损伤或污染异常时先让载台承托晶圆，停止并隔离治具。请以不含客户晶圆图像、工艺机密或个人信息的方式报告风险；敏感细节不要直接发到公开 issue。

Provided as-is, without warranty. The licences and notices describe the legal terms; this page records engineering limitations rather than certification.
