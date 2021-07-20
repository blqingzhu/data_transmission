CREATE TABLE `tb_termination_info`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id 自增',
  `termination_id` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '终端id',
  `lon_lat` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '最近一次经纬度信息，逗号隔开',
  `oilConsume` double(32, 2) NULL DEFAULT NULL COMMENT '最近一次累计油耗',
  `workHours` double(32, 2) NULL DEFAULT NULL COMMENT '最近一次累计工时',
  `prompt_time` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '最近一次上报时间',
  `creator` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '创建人',
  `create_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) COMMENT '创建时间',
  `modify_time` datetime(0) NULL DEFAULT CURRENT_TIMESTAMP(0) ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '修改时间',
   constraint id_unique unique(termination_id),
   PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 18282 CHARACTER SET = utf8mb4  collate=utf8mb4_general_ci COMMENT = '终端基础表' ROW_FORMAT = Dynamic;