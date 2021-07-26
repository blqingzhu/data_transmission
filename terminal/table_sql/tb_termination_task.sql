CREATE TABLE `tb_termination_task`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id 自增',
  `task_id`varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '任务id',
  `termination_id` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '终端id',
  `task_lonlat` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '任务经纬度信息，逗号隔开',
  `step` int(11) NOT NULL  COMMENT '任务步数',
  `status` int(11) NULL DEFAULT NULL COMMENT '0初始 1运行 2成功 3失败',
  `creator` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `create_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `modify_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
   constraint id_unique unique(task_id,termination_id),
   PRIMARY KEY (`id`) USING BTREE,
   constraint FK_Name foreign key (termination_id) references tb_termination_info(termination_id) on delete cascade on update cascade
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 collate=utf8mb4_general_ci COMMENT = '终端任务表' ROW_FORMAT = Dynamic;