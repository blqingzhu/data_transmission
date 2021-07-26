CREATE TABLE `tb_termination_task_history`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id 自增',
  `task_id` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '任务id',
  `json` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '上传的位置信息,json格式',
  `status` int(11) NULL DEFAULT NULL COMMENT '0成功 1失败',
  `create_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `modify_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
  PRIMARY KEY (`id`) USING BTREE,
	constraint HT_Name foreign key (task_id) references tb_termination_task(task_id) on delete cascade on update cascade
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4  COMMENT = '终端历史记录表' ROW_FORMAT = Dynamic;