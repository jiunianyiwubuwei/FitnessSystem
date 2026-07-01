/*
 Navicat Premium Data Transfer

 Source Server         : text1
 Source Server Type    : MySQL
 Source Server Version : 80041 (8.0.41)
 Source Host           : localhost:3306
 Source Schema         : health

 Target Server Type    : MySQL
 Target Server Version : 80041 (8.0.41)
 File Encoding         : 65001

 Date: 13/09/2025 16:14:40
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id` ASC, `codename` ASC) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 61 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO `auth_permission` VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO `auth_permission` VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO `auth_permission` VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO `auth_permission` VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO `auth_permission` VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO `auth_permission` VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO `auth_permission` VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO `auth_permission` VALUES (25, 'Can add calorie record', 7, 'add_calorierecord');
INSERT INTO `auth_permission` VALUES (26, 'Can change calorie record', 7, 'change_calorierecord');
INSERT INTO `auth_permission` VALUES (27, 'Can delete calorie record', 7, 'delete_calorierecord');
INSERT INTO `auth_permission` VALUES (28, 'Can view calorie record', 7, 'view_calorierecord');
INSERT INTO `auth_permission` VALUES (29, 'Can add sys user', 8, 'add_sysuser');
INSERT INTO `auth_permission` VALUES (30, 'Can change sys user', 8, 'change_sysuser');
INSERT INTO `auth_permission` VALUES (31, 'Can delete sys user', 8, 'delete_sysuser');
INSERT INTO `auth_permission` VALUES (32, 'Can view sys user', 8, 'view_sysuser');
INSERT INTO `auth_permission` VALUES (33, 'Can add sys menu', 9, 'add_sysmenu');
INSERT INTO `auth_permission` VALUES (34, 'Can change sys menu', 9, 'change_sysmenu');
INSERT INTO `auth_permission` VALUES (35, 'Can delete sys menu', 9, 'delete_sysmenu');
INSERT INTO `auth_permission` VALUES (36, 'Can view sys menu', 9, 'view_sysmenu');
INSERT INTO `auth_permission` VALUES (37, 'Can add sys role menu', 10, 'add_sysrolemenu');
INSERT INTO `auth_permission` VALUES (38, 'Can change sys role menu', 10, 'change_sysrolemenu');
INSERT INTO `auth_permission` VALUES (39, 'Can delete sys role menu', 10, 'delete_sysrolemenu');
INSERT INTO `auth_permission` VALUES (40, 'Can view sys role menu', 10, 'view_sysrolemenu');
INSERT INTO `auth_permission` VALUES (41, 'Can add sys role', 11, 'add_sysrole');
INSERT INTO `auth_permission` VALUES (42, 'Can change sys role', 11, 'change_sysrole');
INSERT INTO `auth_permission` VALUES (43, 'Can delete sys role', 11, 'delete_sysrole');
INSERT INTO `auth_permission` VALUES (44, 'Can view sys role', 11, 'view_sysrole');
INSERT INTO `auth_permission` VALUES (45, 'Can add sys user role', 12, 'add_sysuserrole');
INSERT INTO `auth_permission` VALUES (46, 'Can change sys user role', 12, 'change_sysuserrole');
INSERT INTO `auth_permission` VALUES (47, 'Can delete sys user role', 12, 'delete_sysuserrole');
INSERT INTO `auth_permission` VALUES (48, 'Can view sys user role', 12, 'view_sysuserrole');
INSERT INTO `auth_permission` VALUES (49, 'Can add health news', 13, 'add_healthnews');
INSERT INTO `auth_permission` VALUES (50, 'Can change health news', 13, 'change_healthnews');
INSERT INTO `auth_permission` VALUES (51, 'Can delete health news', 13, 'delete_healthnews');
INSERT INTO `auth_permission` VALUES (52, 'Can view health news', 13, 'view_healthnews');
INSERT INTO `auth_permission` VALUES (53, 'Can add health data', 14, 'add_healthdata');
INSERT INTO `auth_permission` VALUES (54, 'Can change health data', 14, 'change_healthdata');
INSERT INTO `auth_permission` VALUES (55, 'Can delete health data', 14, 'delete_healthdata');
INSERT INTO `auth_permission` VALUES (56, 'Can view health data', 14, 'view_healthdata');
INSERT INTO `auth_permission` VALUES (57, 'Can add evaluation', 15, 'add_evaluation');
INSERT INTO `auth_permission` VALUES (58, 'Can change evaluation', 15, 'change_evaluation');
INSERT INTO `auth_permission` VALUES (59, 'Can delete evaluation', 15, 'delete_evaluation');
INSERT INTO `auth_permission` VALUES (60, 'Can view evaluation', 15, 'view_evaluation');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_user
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id` ASC, `group_id` ASC) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id` ASC) USING BTREE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id` ASC) USING BTREE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content_type_id` int NULL DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id` ASC) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_auth_user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_chk_1` CHECK (`action_flag` >= 0)
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label` ASC, `model` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (7, 'fitness', 'calorierecord');
INSERT INTO `django_content_type` VALUES (15, 'healthview', 'evaluation');
INSERT INTO `django_content_type` VALUES (14, 'healthview', 'healthdata');
INSERT INTO `django_content_type` VALUES (13, 'healthview', 'healthnews');
INSERT INTO `django_content_type` VALUES (9, 'menu', 'sysmenu');
INSERT INTO `django_content_type` VALUES (10, 'menu', 'sysrolemenu');
INSERT INTO `django_content_type` VALUES (11, 'role', 'sysrole');
INSERT INTO `django_content_type` VALUES (12, 'role', 'sysuserrole');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');
INSERT INTO `django_content_type` VALUES (8, 'user', 'sysuser');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 31 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2025-04-25 02:08:40.662354');
INSERT INTO `django_migrations` VALUES (2, 'auth', '0001_initial', '2025-04-25 02:08:41.820442');
INSERT INTO `django_migrations` VALUES (3, 'admin', '0001_initial', '2025-04-25 02:08:42.060198');
INSERT INTO `django_migrations` VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2025-04-25 02:08:42.070712');
INSERT INTO `django_migrations` VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2025-04-25 02:08:42.080478');
INSERT INTO `django_migrations` VALUES (6, 'contenttypes', '0002_remove_content_type_name', '2025-04-25 02:08:42.232016');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2025-04-25 02:08:42.332917');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0003_alter_user_email_max_length', '2025-04-25 02:08:42.363003');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0004_alter_user_username_opts', '2025-04-25 02:08:42.372148');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0005_alter_user_last_login_null', '2025-04-25 02:08:42.452286');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0006_require_contenttypes_0002', '2025-04-25 02:08:42.460371');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2025-04-25 02:08:42.470400');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0008_alter_user_username_max_length', '2025-04-25 02:08:42.579009');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2025-04-25 02:08:42.685054');
INSERT INTO `django_migrations` VALUES (15, 'auth', '0010_alter_group_name_max_length', '2025-04-25 02:08:42.707522');
INSERT INTO `django_migrations` VALUES (16, 'auth', '0011_update_proxy_permissions', '2025-04-25 02:08:42.717612');
INSERT INTO `django_migrations` VALUES (17, 'auth', '0012_alter_user_first_name_max_length', '2025-04-25 02:08:42.819156');
INSERT INTO `django_migrations` VALUES (18, 'user', '0001_initial', '2025-05-01 10:33:38.061152');
INSERT INTO `django_migrations` VALUES (19, 'fitness', '0001_initial', '2025-05-04 07:30:03.655807');
INSERT INTO `django_migrations` VALUES (20, 'healthview', '0001_initial', '2025-05-04 16:59:16.000000');
INSERT INTO `django_migrations` VALUES (21, 'healthview', '0002_healthdata_calories_burned_healthdata_exercise_count', '2025-05-04 08:59:34.441733');
INSERT INTO `django_migrations` VALUES (22, 'healthview', '0003_remove_healthdata_calories_burned_and_more', '2025-05-04 17:03:22.000000');
INSERT INTO `django_migrations` VALUES (23, 'role', '0001_initial', '2025-05-04 17:06:42.000000');
INSERT INTO `django_migrations` VALUES (24, 'menu', '0001_initial', '2025-05-04 17:07:28.000000');
INSERT INTO `django_migrations` VALUES (25, 'sessions', '0001_initial', '2025-05-04 09:07:37.030012');
INSERT INTO `django_migrations` VALUES (26, 'fitness', '0002_calorierecord_user_alter_calorierecord_table', '2025-05-05 05:56:57.315598');
INSERT INTO `django_migrations` VALUES (27, 'fitness', '0003_remove_calorierecord_user_calorierecord_user_id', '2025-05-05 07:52:12.760463');
INSERT INTO `django_migrations` VALUES (28, 'fitness', '0004_alter_calorierecord_id_alter_calorierecord_user_id', '2025-05-05 12:30:48.140123');
INSERT INTO `django_migrations` VALUES (29, 'fitness', '0002_alter_calorierecord_table', '2025-05-06 12:22:28.786255');
INSERT INTO `django_migrations` VALUES (30, 'fitness', '0003_rename_user_id_calorierecord_user', '2025-05-06 16:56:01.419873');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of django_session
-- ----------------------------

-- ----------------------------
-- Table structure for evaluations
-- ----------------------------
DROP TABLE IF EXISTS `evaluations`;
CREATE TABLE `evaluations`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键',
  `parent_id` int NULL DEFAULT NULL COMMENT '父级评论ID',
  `commenter_id` int NULL DEFAULT NULL COMMENT '评论者ID',
  `replier_id` int NULL DEFAULT NULL COMMENT '回复者ID',
  `content_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '内容类型',
  `content_id` int NULL DEFAULT NULL COMMENT '内容ID',
  `content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '评论内容',
  `upvote_list` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL COMMENT '点赞列表，以\",\"分割',
  `create_time` datetime NULL DEFAULT NULL COMMENT '评论时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 185 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of evaluations
-- ----------------------------
INSERT INTO `evaluations` VALUES (7, 4, 3, NULL, 'NEWS', 10, '大侠风范', '1,7,8,3', '2024-06-08 17:06:19');
INSERT INTO `evaluations` VALUES (8, 1, 3, 3, 'NEWS', 10, '一派胡言', '1,7,8', '2024-06-08 17:06:19');
INSERT INTO `evaluations` VALUES (13, 1, 3, 7, 'NEWS', 10, '这么神奇？', '1,8', '2024-06-08 17:06:19');
INSERT INTO `evaluations` VALUES (23, NULL, 3, NULL, 'NEWS', 10, '我的评论', '3', '2024-05-24 16:24:14');
INSERT INTO `evaluations` VALUES (27, 23, 3, 3, 'NEWS', 10, '什么事情', '3', '2024-05-25 00:32:16');
INSERT INTO `evaluations` VALUES (29, 14, 3, NULL, 'NEWS', 10, '先生。', '3', '2024-05-25 15:08:06');
INSERT INTO `evaluations` VALUES (40, NULL, 3, NULL, 'NEWS', 19, '测试评论啊', '3', '2024-06-13 19:57:02');
INSERT INTO `evaluations` VALUES (44, 40, 3, NULL, 'NEWS', 19, '回复', NULL, '2024-06-13 20:17:20');
INSERT INTO `evaluations` VALUES (45, 40, 3, 3, 'NEWS', 19, '回复', '3', '2024-06-13 20:19:11');
INSERT INTO `evaluations` VALUES (47, 40, 3, 3, 'NEWS', 19, '测试UU', '3', '2024-06-13 20:19:51');
INSERT INTO `evaluations` VALUES (48, 11, 3, NULL, 'NEWS', 10, '哈哈哈哈', NULL, '2024-06-13 20:20:45');
INSERT INTO `evaluations` VALUES (49, NULL, 3, NULL, 'NEWS', 10, 'UUUIII', NULL, '2024-06-13 20:21:24');
INSERT INTO `evaluations` VALUES (50, 49, 3, NULL, 'NEWS', 10, '就是', NULL, '2024-06-13 20:21:30');
INSERT INTO `evaluations` VALUES (51, 4, 3, NULL, 'NEWS', 10, '就是', NULL, '2024-06-13 20:24:40');
INSERT INTO `evaluations` VALUES (52, 4, 3, 8, 'NEWS', 10, '哈哈哈', '3', '2024-06-13 20:24:51');
INSERT INTO `evaluations` VALUES (53, 49, 3, 3, 'NEWS', 10, '哈哈哈', NULL, '2024-06-13 20:32:37');
INSERT INTO `evaluations` VALUES (54, NULL, 3, NULL, 'NEWS', 18, '测试', NULL, '2024-06-13 20:37:26');
INSERT INTO `evaluations` VALUES (55, 54, 3, NULL, 'NEWS', 18, 'niaho ', NULL, '2024-06-13 20:37:36');
INSERT INTO `evaluations` VALUES (58, 57, 3, NULL, 'NEWS', 19, '4324234', NULL, '2024-06-13 20:39:02');
INSERT INTO `evaluations` VALUES (59, 57, 3, 3, 'NEWS', 19, '54354354', NULL, '2024-06-13 20:39:07');
INSERT INTO `evaluations` VALUES (61, NULL, 3, NULL, 'NEWS', 19, '432432423', NULL, '2024-06-13 20:39:29');
INSERT INTO `evaluations` VALUES (83, NULL, 3, NULL, 'NEWS', 13, '健康', NULL, '2024-06-15 02:12:55');
INSERT INTO `evaluations` VALUES (84, NULL, 3, NULL, 'NEWS', 13, '丝滑', NULL, '2024-06-15 02:13:08');
INSERT INTO `evaluations` VALUES (85, NULL, 3, NULL, 'NEWS', 14, '哈哈哈哈哈', NULL, '2024-06-15 02:13:39');
INSERT INTO `evaluations` VALUES (87, NULL, 3, NULL, 'NEWS', 16, '？？？', NULL, '2024-06-15 02:37:10');
INSERT INTO `evaluations` VALUES (88, NULL, 3, NULL, 'NEWS', 16, '好好说话', NULL, '2024-06-15 21:38:26');
INSERT INTO `evaluations` VALUES (89, NULL, 3, NULL, 'NEWS', 19, '12121', '3', '2024-06-17 00:05:02');
INSERT INTO `evaluations` VALUES (90, 89, 3, NULL, 'NEWS', 19, '同意同意', NULL, '2024-06-17 00:05:11');
INSERT INTO `evaluations` VALUES (91, 89, 3, 3, 'NEWS', 19, '323232', NULL, '2024-06-17 00:05:18');
INSERT INTO `evaluations` VALUES (92, NULL, 3, NULL, 'NEWS', 16, '323213', NULL, '2024-06-24 23:53:41');
INSERT INTO `evaluations` VALUES (93, NULL, 3, NULL, 'NEWS', 20, '3123213213', NULL, '2024-06-24 23:53:48');
INSERT INTO `evaluations` VALUES (94, 93, 3, NULL, 'NEWS', 20, '32132132', NULL, '2024-06-24 23:53:53');
INSERT INTO `evaluations` VALUES (98, 95, 3, NULL, 'NEWS', 15, '32132', NULL, '2024-06-24 23:54:38');
INSERT INTO `evaluations` VALUES (99, 95, 3, NULL, 'NEWS', 15, '43434', NULL, '2024-06-24 23:54:41');
INSERT INTO `evaluations` VALUES (100, 95, 3, 3, 'NEWS', 15, '432423433454354', NULL, '2024-06-24 23:54:45');
INSERT INTO `evaluations` VALUES (101, NULL, 3, NULL, 'NEWS', 15, '4324324', NULL, '2024-06-24 23:54:52');
INSERT INTO `evaluations` VALUES (102, NULL, 3, NULL, 'NEWS', 20, '2121', NULL, '2024-06-30 23:09:39');
INSERT INTO `evaluations` VALUES (103, NULL, 3, NULL, 'NEWS', 16, '43434', NULL, '2024-06-30 23:09:49');
INSERT INTO `evaluations` VALUES (104, NULL, 3, NULL, 'NEWS', 20, '4343', NULL, '2024-07-07 03:00:30');
INSERT INTO `evaluations` VALUES (106, NULL, 3, NULL, 'NEWS', 20, '2121', NULL, '2024-07-07 04:46:11');
INSERT INTO `evaluations` VALUES (107, NULL, 3, NULL, 'NEWS', 20, '测试', NULL, '2024-07-07 04:46:25');
INSERT INTO `evaluations` VALUES (110, 109, 17, NULL, 'NEWS', 10, 'dsdsds', NULL, '2024-07-08 14:09:37');
INSERT INTO `evaluations` VALUES (112, 111, 9, NULL, 'NEWS', 5, '4324322', NULL, '2024-07-14 15:17:44');
INSERT INTO `evaluations` VALUES (113, 111, 9, 9, 'NEWS', 5, '5435435', NULL, '2024-07-14 15:17:51');
INSERT INTO `evaluations` VALUES (115, NULL, 9, NULL, 'NEWS', 2, '221332131', NULL, '2024-07-14 15:21:54');
INSERT INTO `evaluations` VALUES (116, NULL, 9, NULL, 'NEWS', 3, '这是指标的评论！', NULL, '2024-07-14 15:22:13');
INSERT INTO `evaluations` VALUES (117, NULL, 9, NULL, 'NEWS', 5, '3232', NULL, '2024-07-14 19:20:56');
INSERT INTO `evaluations` VALUES (118, 117, 9, NULL, 'NEWS', 5, '4324324', NULL, '2024-07-14 19:21:01');
INSERT INTO `evaluations` VALUES (119, NULL, 9, NULL, 'NEWS', 12, '3342143', '9', '2024-07-16 16:27:51');
INSERT INTO `evaluations` VALUES (120, 119, 9, NULL, 'NEWS', 12, '43243243', '9', '2024-07-16 16:27:56');
INSERT INTO `evaluations` VALUES (121, 119, 9, 9, 'NEWS', 12, '432423432', '9', '2024-07-16 16:28:01');
INSERT INTO `evaluations` VALUES (124, NULL, 3, NULL, 'NEWS', 12, '所以，为了自己，为了家人，为了亲朋，保健养生从现在做起！在这个充满挑战和机遇的时代里，让我们一起携手前行，用补肽这一健康管理利器守护我们的健康之路。', NULL, '2024-11-18 20:28:08');
INSERT INTO `evaluations` VALUES (125, 119, 3, 9, 'NEWS', 12, '所以，为了自己，为了家人，为了亲朋，保健养生从现在做起！在这个充满挑战和机遇的时代里，让我们一起携手前行，用补肽这一健康管理利器守护我们的健康之路。', '3', '2024-11-18 20:28:14');
INSERT INTO `evaluations` VALUES (126, NULL, 1, NULL, 'news', 1, '666', '[]', '2025-03-15 18:41:14');
INSERT INTO `evaluations` VALUES (127, NULL, 1, NULL, 'news', 1, '666', '[]', '2025-03-15 18:41:40');
INSERT INTO `evaluations` VALUES (128, NULL, 1, NULL, 'news', 1, '牛逼', '[]', '2025-03-15 18:48:49');
INSERT INTO `evaluations` VALUES (129, NULL, 1, NULL, 'news', 1, '可以吗', '[]', '2025-03-15 19:06:56');
INSERT INTO `evaluations` VALUES (130, 129, 22, NULL, 'news', 1, '挺牛的', '[]', '2025-03-15 19:35:15');
INSERT INTO `evaluations` VALUES (131, NULL, 22, NULL, 'news', 1, '牛的', '[]', '2025-03-15 19:35:43');
INSERT INTO `evaluations` VALUES (132, 126, 22, NULL, 'news', 1, '干涉么', '[]', '2025-03-15 19:35:58');
INSERT INTO `evaluations` VALUES (133, 129, 22, NULL, 'news', 1, '牛逼', '[]', '2025-03-15 19:41:16');
INSERT INTO `evaluations` VALUES (134, NULL, 22, NULL, 'news', 1, 'jjkkooo', '[]', '2025-03-16 16:50:13');
INSERT INTO `evaluations` VALUES (135, 134, 22, NULL, 'news', 1, 'wssw', '[]', '2025-03-16 16:50:22');
INSERT INTO `evaluations` VALUES (137, NULL, 22, NULL, 'news', 6, '睡不着怎么办', '[]', '2025-03-18 17:49:28');
INSERT INTO `evaluations` VALUES (138, NULL, 29, NULL, 'news', 2, '测试', '[]', '2025-03-21 07:44:58');
INSERT INTO `evaluations` VALUES (139, NULL, 22, NULL, 'news', 2, '11', '[]', '2025-03-21 07:53:03');
INSERT INTO `evaluations` VALUES (140, NULL, 29, NULL, 'news', 2, '111', '[]', '2025-03-21 08:04:48');
INSERT INTO `evaluations` VALUES (141, NULL, 29, NULL, 'news', 3, '测试', '[]', '2025-03-21 08:10:37');
INSERT INTO `evaluations` VALUES (142, NULL, 29, NULL, 'news', 5, '测试', '[]', '2025-03-21 08:10:49');
INSERT INTO `evaluations` VALUES (143, 142, 29, NULL, 'news', 5, '成功', '[]', '2025-03-21 08:10:55');
INSERT INTO `evaluations` VALUES (144, NULL, 29, NULL, 'news', 2, '现在', '[]', '2025-03-21 09:37:40');
INSERT INTO `evaluations` VALUES (145, NULL, 22, NULL, 'news', 1, '666', '[]', '2025-04-08 12:57:39');
INSERT INTO `evaluations` VALUES (146, NULL, 30, NULL, 'news', 11, '666', '[]', '2025-04-25 02:55:20');
INSERT INTO `evaluations` VALUES (147, NULL, 30, NULL, 'news', 1, '666', '[]', '2025-04-29 08:12:15');
INSERT INTO `evaluations` VALUES (148, NULL, 31, NULL, 'news', 4, '测试', '[]', '2025-05-07 08:21:39');
INSERT INTO `evaluations` VALUES (149, NULL, 30, NULL, 'news', 2, '666', '[]', '2025-05-07 14:27:41');
INSERT INTO `evaluations` VALUES (150, 144, 30, NULL, 'news', 2, '666', '[]', '2025-05-07 14:27:52');
INSERT INTO `evaluations` VALUES (151, NULL, 30, NULL, 'news', 2, '777', '[]', '2025-05-07 14:29:35');
INSERT INTO `evaluations` VALUES (152, 149, 30, NULL, 'news', 2, '777', '[]', '2025-05-07 14:29:50');
INSERT INTO `evaluations` VALUES (153, NULL, 30, NULL, 'news', 2, '666', '[]', '2025-05-07 14:32:20');
INSERT INTO `evaluations` VALUES (177, NULL, 30, NULL, 'news', 5, '好好好', '[]', '2025-05-08 08:30:50');
INSERT INTO `evaluations` VALUES (178, 142, 30, NULL, 'news', 5, '耶耶耶', '[]', '2025-05-08 08:31:01');
INSERT INTO `evaluations` VALUES (179, NULL, 30, NULL, 'news', 5, '777', '[]', '2025-05-08 08:43:52');
INSERT INTO `evaluations` VALUES (180, 142, 30, NULL, 'news', 5, '好好好', '[]', '2025-05-08 08:44:04');
INSERT INTO `evaluations` VALUES (181, NULL, 30, NULL, 'news', 5, '777', '[]', '2025-05-08 08:49:48');
INSERT INTO `evaluations` VALUES (182, 142, 30, NULL, 'news', 5, '666', '[]', '2025-05-08 08:50:02');
INSERT INTO `evaluations` VALUES (183, NULL, 30, NULL, 'news', 4, '好好好', '[]', '2025-05-27 10:46:26');
INSERT INTO `evaluations` VALUES (184, NULL, 30, NULL, 'news', 1, '666', '[]', '2025-05-27 16:37:23');

-- ----------------------------
-- Table structure for fitness_calorierecord
-- ----------------------------
DROP TABLE IF EXISTS `fitness_calorierecord`;
CREATE TABLE `fitness_calorierecord`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `exercise_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `weight` double NOT NULL,
  `counter` int NOT NULL,
  `calories` double NOT NULL,
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `fitness_calorierecord_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 109 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of fitness_calorierecord
-- ----------------------------
INSERT INTO `fitness_calorierecord` VALUES (2, 30, 'pull-up', 65, 4, 8.3, '2025-05-05 20:09:46.000000');
INSERT INTO `fitness_calorierecord` VALUES (3, 30, 'pull-up', 65, 3, 7.96, '2025-05-05 19:30:14.000000');
INSERT INTO `fitness_calorierecord` VALUES (4, 30, 'pull-up', 65, 22, 40.52, '2025-05-06 17:05:20.000000');
INSERT INTO `fitness_calorierecord` VALUES (5, 30, 'pull-up', 65, 5, 9.21, '2025-05-06 17:10:50.000000');
INSERT INTO `fitness_calorierecord` VALUES (6, 30, 'push-up', 65, 10, 5.78, '2025-05-06 17:18:18.000000');
INSERT INTO `fitness_calorierecord` VALUES (7, 30, 'push-up', 65, 10, 5.78, '2025-05-06 17:26:53.881631');
INSERT INTO `fitness_calorierecord` VALUES (8, 30, 'push-up', 65, 10, 5.78, '2025-05-06 17:29:28.000000');
INSERT INTO `fitness_calorierecord` VALUES (9, 30, 'push-up', 65, 10, 5.78, '2025-05-06 17:36:16.000000');
INSERT INTO `fitness_calorierecord` VALUES (10, 30, 'push-up', 65, 10, 5.78, '2025-05-07 17:39:09.000000');
INSERT INTO `fitness_calorierecord` VALUES (11, 30, 'push-up', 65, 5, 2.89, '2025-05-07 17:42:15.000000');
INSERT INTO `fitness_calorierecord` VALUES (39, 30, 'pull-up', 65, 5, 9.21, '2025-05-07 03:11:27.329284');
INSERT INTO `fitness_calorierecord` VALUES (40, 30, 'pull-up', 65, 5, 9.21, '2025-05-07 03:20:00.330119');
INSERT INTO `fitness_calorierecord` VALUES (41, 30, 'pull-up', 65, 5, 9.21, '2025-05-07 04:08:52.011631');
INSERT INTO `fitness_calorierecord` VALUES (42, 30, 'pull-up', 65, 5, 9.21, '2025-05-07 04:12:58.167802');
INSERT INTO `fitness_calorierecord` VALUES (43, 30, 'push-up', 65, 7, 4.04, '2025-05-07 15:04:28.204139');
INSERT INTO `fitness_calorierecord` VALUES (44, 30, 'push-up', 65, 10, 5.78, '2025-05-07 15:09:13.567649');
INSERT INTO `fitness_calorierecord` VALUES (45, 30, 'pull-up', 65, 5, 9.21, '2025-05-07 15:10:50.395596');
INSERT INTO `fitness_calorierecord` VALUES (46, 30, 'push-up', 62, 10, 5.51, '2025-05-07 15:16:15.371888');
INSERT INTO `fitness_calorierecord` VALUES (47, 30, 'pull-up', 65, 5, 9.21, '2025-05-08 04:43:34.175204');
INSERT INTO `fitness_calorierecord` VALUES (48, 30, 'push-up', 65, 10, 5.78, '2025-05-08 04:44:12.962068');
INSERT INTO `fitness_calorierecord` VALUES (49, 30, 'push-up', 65, 1, 0.58, '2025-05-08 04:44:37.424041');
INSERT INTO `fitness_calorierecord` VALUES (50, 30, 'jumping-jack', 65, 0, 0, '2025-05-08 04:44:43.820608');
INSERT INTO `fitness_calorierecord` VALUES (51, 30, 'pull-up', 65, 4, 7.37, '2025-05-08 04:46:00.011469');
INSERT INTO `fitness_calorierecord` VALUES (52, 30, 'push-up', 65, 10, 5.78, '2025-05-08 04:47:05.051036');
INSERT INTO `fitness_calorierecord` VALUES (53, 30, 'push-up', 65, 10, 5.78, '2025-05-08 08:17:44.002103');
INSERT INTO `fitness_calorierecord` VALUES (54, 30, 'pull-up', 65, 5, 9.21, '2025-05-08 08:19:52.257325');
INSERT INTO `fitness_calorierecord` VALUES (55, 30, 'pull-up', 65, 3, 5.53, '2025-05-08 08:25:27.895147');
INSERT INTO `fitness_calorierecord` VALUES (56, 30, 'pull-up', 65, 5, 9.21, '2025-05-08 08:26:51.928619');
INSERT INTO `fitness_calorierecord` VALUES (57, 30, 'push-up', 65, 10, 5.78, '2025-05-08 08:34:31.438854');
INSERT INTO `fitness_calorierecord` VALUES (58, 30, 'pull-up', 65, 5, 9.21, '2025-05-08 08:36:03.119208');
INSERT INTO `fitness_calorierecord` VALUES (59, 30, 'push-up', 65, 8, 4.62, '2025-05-08 08:46:55.679900');
INSERT INTO `fitness_calorierecord` VALUES (60, 30, 'pull-up', 65, 5, 9.21, '2025-05-08 08:48:24.608561');
INSERT INTO `fitness_calorierecord` VALUES (61, 30, 'push-up', 65, 10, 5.78, '2025-05-08 08:53:03.543128');
INSERT INTO `fitness_calorierecord` VALUES (62, 30, 'pull-up', 65, 5, 9.21, '2025-05-08 08:54:39.407600');
INSERT INTO `fitness_calorierecord` VALUES (63, 30, 'pull-up', 65, 5, 9.21, '2025-06-03 06:16:34.086630');
INSERT INTO `fitness_calorierecord` VALUES (64, 30, 'pull-up', 65, 2, 3.68, '2025-06-05 12:37:18.151419');
INSERT INTO `fitness_calorierecord` VALUES (65, 30, 'push-up', 65, 2, 1.16, '2025-06-06 03:32:01.782527');
INSERT INTO `fitness_calorierecord` VALUES (66, 30, 'push-up', 65, 3, 1.73, '2025-06-11 09:23:40.865571');
INSERT INTO `fitness_calorierecord` VALUES (67, 30, 'push-up', 65, 2, 1.16, '2025-06-11 09:39:20.234956');
INSERT INTO `fitness_calorierecord` VALUES (68, 30, 'pull-up', 65, 22, 40.52, '2025-06-11 09:59:49.401837');
INSERT INTO `fitness_calorierecord` VALUES (69, 30, 'pull-up', 65, 0, 0, '2025-06-11 10:00:13.569720');
INSERT INTO `fitness_calorierecord` VALUES (70, 30, 'pull-up', 65, 5, 9.21, '2025-06-11 10:13:29.520659');
INSERT INTO `fitness_calorierecord` VALUES (71, 30, 'push-up', 65, 9, 5.2, '2025-06-11 10:30:41.531202');
INSERT INTO `fitness_calorierecord` VALUES (72, 30, 'push-up', 65, 0, 0, '2025-06-11 10:39:31.020266');
INSERT INTO `fitness_calorierecord` VALUES (73, 30, 'push-up', 65, 2, 1.16, '2025-06-11 10:40:03.343193');
INSERT INTO `fitness_calorierecord` VALUES (74, 30, 'push-up', 65, 7, 4.04, '2025-06-11 10:43:49.645316');
INSERT INTO `fitness_calorierecord` VALUES (75, 30, 'push-up', 65, 3, 1.73, '2025-06-11 11:08:03.319135');
INSERT INTO `fitness_calorierecord` VALUES (76, 30, 'push-up', 65, 2, 1.16, '2025-06-11 11:14:33.285469');
INSERT INTO `fitness_calorierecord` VALUES (77, 30, 'push-up', 65, 1, 0.58, '2025-06-11 11:16:07.089232');
INSERT INTO `fitness_calorierecord` VALUES (78, 30, 'push-up', 38, 0, 0, '2025-06-11 12:01:20.242172');
INSERT INTO `fitness_calorierecord` VALUES (79, 30, 'push-up', 38, 0, 0, '2025-06-11 13:37:51.876651');
INSERT INTO `fitness_calorierecord` VALUES (80, 30, 'push-up', 38, 0, 0, '2025-06-11 13:50:09.424522');
INSERT INTO `fitness_calorierecord` VALUES (81, 30, 'push-up', 65, 29, 16.76, '2025-06-11 17:12:34.115861');
INSERT INTO `fitness_calorierecord` VALUES (82, 30, 'push-up', 65, 21, 12.13, '2025-06-11 17:17:27.183023');
INSERT INTO `fitness_calorierecord` VALUES (83, 30, 'push-up', 65, 9, 5.2, '2025-06-11 17:29:40.203401');
INSERT INTO `fitness_calorierecord` VALUES (84, 30, 'pull-up', 65, 0, 0, '2025-06-11 17:37:22.711206');
INSERT INTO `fitness_calorierecord` VALUES (85, 30, 'push-up', 65, 1, 0.58, '2025-06-11 17:37:44.364160');
INSERT INTO `fitness_calorierecord` VALUES (86, 30, 'push-up', 65, 1, 0.58, '2025-06-11 17:39:11.988173');
INSERT INTO `fitness_calorierecord` VALUES (87, 30, 'pull-up', 65, 7, 12.89, '2025-06-11 17:40:04.589704');
INSERT INTO `fitness_calorierecord` VALUES (88, 30, 'push-up', 65, 0, 0, '2025-06-11 18:05:35.837938');
INSERT INTO `fitness_calorierecord` VALUES (89, 30, 'push-up', 65, 2, 1.16, '2025-06-11 18:06:14.230684');
INSERT INTO `fitness_calorierecord` VALUES (90, 30, 'push-up', 65, 1, 0.58, '2025-06-11 18:06:48.198092');
INSERT INTO `fitness_calorierecord` VALUES (91, 30, 'push-up', 65, 0, 0, '2025-06-12 16:37:27.714213');
INSERT INTO `fitness_calorierecord` VALUES (92, 30, 'push-up', 65, 7, 4.04, '2025-06-12 17:16:45.187429');
INSERT INTO `fitness_calorierecord` VALUES (93, 30, 'push-up', 65, 8, 4.62, '2025-06-12 17:29:37.695977');
INSERT INTO `fitness_calorierecord` VALUES (94, 30, 'push-up', 65, 1, 0.58, '2025-06-12 17:42:32.474652');
INSERT INTO `fitness_calorierecord` VALUES (95, 30, 'push-up', 65, 6, 3.47, '2025-06-13 11:51:38.690268');
INSERT INTO `fitness_calorierecord` VALUES (96, 30, 'push-up', 65, 38, 21.96, '2025-06-13 12:02:19.245569');
INSERT INTO `fitness_calorierecord` VALUES (97, 30, 'push-up', 65, 0, 0, '2025-06-13 14:03:29.226655');
INSERT INTO `fitness_calorierecord` VALUES (98, 30, 'push-up', 65, 0, 0, '2025-06-13 14:06:12.829228');
INSERT INTO `fitness_calorierecord` VALUES (99, 30, 'push-up', 65, 9, 5.2, '2025-06-13 15:24:38.912596');
INSERT INTO `fitness_calorierecord` VALUES (100, 30, 'push-up', 65, 21, 12.13, '2025-06-13 15:38:44.396911');
INSERT INTO `fitness_calorierecord` VALUES (101, 30, 'push-up', 65, 3, 1.73, '2025-06-13 15:42:17.834963');
INSERT INTO `fitness_calorierecord` VALUES (102, 30, 'push-up', 65, 0, 0, '2025-06-13 15:53:17.189765');
INSERT INTO `fitness_calorierecord` VALUES (103, 30, 'pull-up', 65, 4, 7.37, '2025-06-16 13:10:22.347852');
INSERT INTO `fitness_calorierecord` VALUES (104, 30, 'pull-up', 65, 9, 16.57, '2025-06-16 13:11:10.246994');
INSERT INTO `fitness_calorierecord` VALUES (105, 30, 'pull-up', 65, 0, 0, '2025-06-16 13:12:53.159082');
INSERT INTO `fitness_calorierecord` VALUES (106, 30, 'push-up', 65, 2, 1.16, '2025-07-19 17:22:38.268233');
INSERT INTO `fitness_calorierecord` VALUES (107, 30, 'push-up', 65, 1, 0.58, '2025-09-07 15:44:39.770653');
INSERT INTO `fitness_calorierecord` VALUES (108, 30, 'push-up', 65, 4, 2.31, '2025-09-13 07:59:43.353335');

-- ----------------------------
-- Table structure for health_data
-- ----------------------------
DROP TABLE IF EXISTS `health_data`;
CREATE TABLE `health_data`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '关联用户ID',
  `weight` float NOT NULL COMMENT '体重',
  `sleep_hours` float NOT NULL COMMENT '睡眠时长',
  `exercise_time` int NOT NULL COMMENT '运动时长',
  `feedback` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '健康反馈',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '打卡时间',
  `exercise_type` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '运动类型',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `health_data_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 49 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '健康数据表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of health_data
-- ----------------------------
INSERT INTO `health_data` VALUES (1, 1, 80, 8, 50, '今天运动效果不错，继续保持！', '2025-03-16 18:24:42', NULL);
INSERT INTO `health_data` VALUES (2, 3, 70, 8, 50, '今天运动效果不错，继续保持！', '2025-03-16 18:25:04', NULL);
INSERT INTO `health_data` VALUES (6, 1, 40, 7, 60, '今天运动效果不错，继续保持！', '2025-03-16 18:25:53', NULL);
INSERT INTO `health_data` VALUES (8, 3, 40, 7, 60, '今天运动效果不错，继续保持！', '2025-03-16 18:26:59', NULL);
INSERT INTO `health_data` VALUES (9, 3, 40, 7, 80, '今天运动效果不错，继续保持！', '2025-03-16 18:27:06', NULL);
INSERT INTO `health_data` VALUES (10, 22, 70, 8, 50, '身体状态良好，继续保持！', '2025-03-16 10:40:42', NULL);
INSERT INTO `health_data` VALUES (11, 22, 50, 8, 50, '身体状态良好，继续保持！', '2025-03-16 10:42:54', NULL);
INSERT INTO `health_data` VALUES (12, 22, 33, 7, 50, '身体状态良好，继续保持！', '2025-03-16 10:43:11', NULL);
INSERT INTO `health_data` VALUES (13, 22, 80, 7, 13, '运动不足，建议每天坚持30分钟以上的有氧运动', '2025-03-16 10:45:13', NULL);
INSERT INTO `health_data` VALUES (14, 22, 59, 7, 80, '身体状态良好，继续保持！', '2025-03-16 10:45:29', NULL);
INSERT INTO `health_data` VALUES (15, 22, 59, 7, 80, '身体状态良好，继续保持！', '2025-03-16 10:45:46', NULL);
INSERT INTO `health_data` VALUES (16, 22, 59, 7, 80, '身体状态良好，继续保持！', '2025-03-16 10:45:49', NULL);
INSERT INTO `health_data` VALUES (17, 22, 59, 7, 80, '身体状态良好，继续保持！', '2025-03-16 10:45:49', NULL);
INSERT INTO `health_data` VALUES (18, 22, 59, 7, 80, '身体状态良好，继续保持！', '2025-03-16 10:45:49', NULL);
INSERT INTO `health_data` VALUES (19, 22, 50, 8, 56, '身体状态良好，继续保持！', '2025-03-16 10:48:41', NULL);
INSERT INTO `health_data` VALUES (20, 22, 59, 7, 70, '身体状态良好，继续保持！', '2025-03-16 10:51:14', NULL);
INSERT INTO `health_data` VALUES (21, 22, 50, 8, 50, '身体状态良好，继续保持！', '2025-04-08 12:59:31', NULL);
INSERT INTO `health_data` VALUES (22, 30, 1, 2, 1, '睡眠不足，请注意调整作息 ', '2025-04-25 02:51:28', '其他');
INSERT INTO `health_data` VALUES (23, 30, 65, 7, 30, '身体状态良好，继续保持！', '2025-04-27 17:29:08', '其他');
INSERT INTO `health_data` VALUES (24, 30, 65, 6.5, 30, '身体状态良好，继续保持！', '2025-04-27 17:29:22', '其他');
INSERT INTO `health_data` VALUES (25, 30, 65, 6.5, 1, '运动不足，建议每天坚持30分钟以上的有氧运动', '2025-04-27 17:29:39', '其他');
INSERT INTO `health_data` VALUES (26, 30, 65, 6.5, 60, '身体状态良好，继续保持！', '2025-04-27 17:29:55', '其他');
INSERT INTO `health_data` VALUES (27, 30, 63, 6.5, 61, '身体状态良好，继续保持！', '2025-04-27 17:30:39', '其他');
INSERT INTO `health_data` VALUES (28, 30, 60, 8, 60, '身体状态良好，继续保持！', '2025-04-28 04:42:53', '其他');
INSERT INTO `health_data` VALUES (29, 30, 62, 5, 0, '睡眠不足，请注意调整作息 ', '2025-04-28 06:48:16', '其他');
INSERT INTO `health_data` VALUES (30, 30, 66, 8, 90, '身体状态良好，继续保持！', '2025-04-28 10:02:27', '其他');
INSERT INTO `health_data` VALUES (31, 30, 62, 8, 120, '身体状态良好，继续保持！', '2025-04-29 05:01:33', '其他');
INSERT INTO `health_data` VALUES (32, 30, 62, 7, 60, '身体状态良好，继续保持！', '2025-04-29 05:30:18', '打篮球');
INSERT INTO `health_data` VALUES (33, 30, 56, 8, 80, '身体状态良好，继续保持！', '2025-04-29 08:14:57', '跑步');
INSERT INTO `health_data` VALUES (34, 30, 55, 6, 30, '身体状态良好，继续保持！', '2025-05-01 05:02:51', '跑步');
INSERT INTO `health_data` VALUES (35, 30, 65, 8, 60, '身体状态良好，继续保持！', '2025-05-04 17:00:10', '打篮球');
INSERT INTO `health_data` VALUES (36, 30, 65, 8, 60, '身体状态良好，继续保持！', '2025-05-07 14:37:42', '打篮球');
INSERT INTO `health_data` VALUES (37, 30, 65, 8, 60, '身体状态良好，继续保持！', '2025-05-07 14:43:09', '游泳');
INSERT INTO `health_data` VALUES (38, 30, 65, 8, 60, '身体状态良好，继续保持！', '2025-05-07 14:52:54', '跑步');
INSERT INTO `health_data` VALUES (39, 30, 65, 8, 30, '身体状态良好，继续保持！', '2025-05-07 14:58:30', '跑步');
INSERT INTO `health_data` VALUES (40, 30, 60, 7, 60, '身体状态良好，继续保持！', '2025-05-07 15:03:08', '打篮球');
INSERT INTO `health_data` VALUES (41, 30, 63, 7, 60, '身体状态良好，继续保持！', '2025-05-07 15:07:55', '游泳');
INSERT INTO `health_data` VALUES (42, 30, 62, 7, 60, '身体状态良好，继续保持！', '2025-05-07 15:14:59', '打篮球');
INSERT INTO `health_data` VALUES (43, 30, 62, 8, 30, '身体状态良好，继续保持！', '2025-05-08 08:15:56', '跑步');
INSERT INTO `health_data` VALUES (44, 30, 65, 8, 40, '身体状态良好，继续保持！', '2025-05-08 08:32:32', '骑自行车');
INSERT INTO `health_data` VALUES (45, 30, 63, 8, 40, '身体状态良好，继续保持！', '2025-05-08 08:45:19', '跳绳');
INSERT INTO `health_data` VALUES (46, 30, 60, 7, 60, '身体状态良好，继续保持！', '2025-05-08 08:51:15', '打篮球');
INSERT INTO `health_data` VALUES (47, 30, 90, 9, 20, '体重偏高，建议多运动和控制饮食 ️', '2025-06-09 07:55:38', '');
INSERT INTO `health_data` VALUES (48, 30, 66, 8, 60, '身体状态良好，继续保持！', '2025-06-11 10:29:44', '跑步');

-- ----------------------------
-- Table structure for news
-- ----------------------------
DROP TABLE IF EXISTS `news`;
CREATE TABLE `news`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '健康资讯ID',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '标题',
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL COMMENT '内容',
  `tag_id` int NULL DEFAULT NULL COMMENT '标签ID',
  `cover` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '图片封面',
  `reader_ids` text CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL COMMENT '阅读者ID列表，用“,”分割',
  `is_top` tinyint(1) NULL DEFAULT NULL COMMENT '是否推荐',
  `create_time` datetime NULL DEFAULT NULL COMMENT '发布时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin COMMENT = '健康资讯表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of news
-- ----------------------------
INSERT INTO `news` VALUES (1, '成年男性平均身高接近1米7，女性1米58', '<p>中国人长高了！</p><p style=\"text-align: justify;\">成年男性平均身高接近1米7，女性1米58</p><p style=\"text-align: justify;\">据介绍，2015年至2019年，国家卫健委组织中国疾控中心、国家癌症中心、国家心血管病中心开展了新一轮中国居民慢性病与营养监测，覆盖全国31个省(区、市)近6亿人口，现场调查人数超过60万，具有国家和省级代表性，根据监测结果编写形成《中国居民营养与慢性病状况报告(2020年)》。</p><p style=\"text-align: justify;\">报告显示，中国居民体格发育与营养不足问题持续改善，城乡差异逐步缩小。中国城乡居民膳食能量和蛋白质、脂肪、碳水化合物三大宏量营养素摄入充足，优质蛋白摄入不断增加。</p><p style=\"text-align: justify;\">另外，近年来，中国人还“长高了”！</p><p style=\"text-align: justify;\">数据显示，中国成人平均身高继续增长，18-44岁男性和女性的平均身高分别为169.7厘米和158.0厘米，与2015年发布结果相比分别增加1.2厘米和0.8厘米。</p><p>儿童青少年生长发育水平持续改善，6-17岁男孩和女孩各年龄组身高均有增加，平均增加值分别为1.6厘米和1.0厘米，6岁以下儿童生长迟缓率降至7%以下，低体重率降至5%以下，均已实现2020年国家规划目标。</p>', 2, 'http://localhost:8000/media/show/13.png', NULL, 0, '2024-07-11 15:40:04');
INSERT INTO `news` VALUES (2, '疾病，就像一位潜藏在暗处的狡猾猎手，随时准备向我们发动攻击', '<p><br></p><p style=\"text-align: justify;\">在过去，随着中国经济的高速发展，许多人的生活水平和物质条件得到了很大的改善。然而，这种快速发展的背后，却隐藏着一些被忽视的问题，其中较为突出的就是健康问题。当经济增速放缓，社会逐渐趋向和谐时，人们开始意识到，健康才是生活中更为重要的一部分。</p><p style=\"text-align: justify;\"><strong>中国人的健康数据，触目惊心！</strong></p><p style=\"text-align: justify;\">经过精心搜集与整理，我们获得了一组关于中国人健康状况的详尽数据。它们不仅仅是冷冰冰的统计结果，更像是一个个鲜活的生命在向我们诉说着健康的宝贵。</p><p style=\"text-align: justify;\">高血压——1.6-1.7亿人</p><p style=\"text-align: justify;\">高血脂——1亿多人</p><p style=\"text-align: justify;\">糖尿病患者——9240万人</p><p style=\"text-align: justify;\">超重或者肥胖症——7000万-----2亿人</p><p style=\"text-align: justify;\">血脂异常——1.6亿人</p><p style=\"text-align: justify;\">脂肪肝患者——1.2亿人</p><p style=\"text-align: justify;\">平均每30秒，就有一个人罹患癌症，</p><p style=\"text-align: justify;\">平均每30秒，就有一个人罹患糖尿病，</p><p style=\"text-align: justify;\">平均每30秒，至少有一个人死于心脑血管疾病。</p><p style=\"text-align: justify;\">这些冰冷的数字背后，是无数家庭的痛苦和无奈。它们无声地诉说着一个残酷的真相：在繁忙的生活中，我们往往为了追逐金钱和物质享受，而忽略了身体的健康。当健康问题如暗流涌动，悄然而至时，我们才如梦初醒，惊觉已为时晚矣！</p><p style=\"text-align: justify;\"><strong>树立良好的健康理念</strong></p><p style=\"text-align: justify;\">快节奏的现代生活，如同一只无形的手，推动着我们不断前行，却也在不经意间，让我们生活方式和饮食习惯发生了很大的变化。作息不规律、高油高盐的饮食等，悄然侵蚀着我们的健康，使得慢性疾病的阴影逐渐笼罩在我们的生活之上。</p><p style=\"text-align: justify;\">更为严峻的是，我们对健康的重视程度仍然远远不够。在过去的日子里，人们紧紧盯着经济的发展和物质条件的改善，却忘记了健康才是生命的根基。我们需要的，不仅仅是医疗技术的日新月异，更需要的是健康理念的深入人心，健康行为的自觉养成。</p><p style=\"text-align: justify;\">健康对于每个人来说都是刻不容缓的。我们要珍惜自己的身体，我们要时刻提醒自己，健康才是重要的，不要等到失去健康之后才后悔莫及。<br></p><p style=\"text-align: justify;\"><strong>补肽刻不容缓</strong></p><p style=\"text-align: justify;\">疾病，就像一位潜藏在暗处的狡猾猎手，随时准备向我们发动攻击。它的存在无声无息，却又无比强大，一旦被我们忽视，便有可能迅速蔓延，成为威胁我们生命安全的熊熊烈火。而补肽，这一健康管理的利器，正是我们对抗疾病、保持健康的重要武器。</p><p style=\"text-align: justify;\">补肽，顾名思义，就是补充身体所需的肽类物质。人体本身就含有小分子肽，但随着年龄的增长，肽类物质会逐渐减少，导致身体各项功能逐渐衰退。因此，及时补充肽类物质，对于保持身体健康具有重要意义。</p><p style=\"text-align: justify;\">小分子肽，如同一位贴心的守护者，为我们的身体健康筑起一道坚实的屏障，让我们在面对外界病邪时更有抵抗力，还能帮助身体更好地吸收营养，预防慢性疾病的发生。</p><p style=\"text-align: justify;\">记住，健康是我们宝贵的财富，只有拥有健康的身体，我们才能更好地享受生活、追求梦想。因为没有了健康，我们就无法享受生活的美好，无法陪伴家人，无法实现自己的梦想。</p><p>所以，为了自己，为了家人，为了亲朋，保健养生从现在做起！在这个充满挑战和机遇的时代里，让我们一起携手前行，用补肽这一健康管理利器守护我们的健康之路。</p>', 2, 'http://localhost:8000/media/show/2.jpg', NULL, 1, '2024-07-03 15:48:00');
INSERT INTO `news` VALUES (3, '身体健康的十项指标，你知道几个？', '<p>随着人们健康意识的提高。有关健康的话题越来越引起重视。不生病就是健康吗？这样说，有点太狭隘了。健康的准确定义应该是身体健康，心理健康，具有良好的社会适应性。今天我们就来详细了解身体健康的十项指标。</p><h4 style=\"text-align: justify;\"><strong>1.饮食指标</strong></h4><p style=\"text-align: justify;\">一般来说成人每天应该吃500克左右的食物，而老人的话，因为肠胃功能减弱，则不应该超过350克。如果出现多食多饮，而且体重下降的情况，就要考虑是否得了糖尿病或者甲亢；如果食量减少 ，每天摄取的食物不到250克，持续时间比较长，就要考虑是否患有炎症或者恶性肿瘤了，要及时检查。</p><p style=\"text-align: justify;\">2.体重指标</p><p style=\"text-align: justify;\">体重并不是越轻越好。这里教给大家一个公式，你可以算下你的正常体重应该是多少。世界卫生组织推荐的计算方法：男性：(身高cm－80)×70﹪=标准体重；女性：(身高cm－70)×60﹪=标准体重。如果短时间内，体重下降过快，人明显消瘦，这种情况多见于糖尿病、甲亢、恶性肿瘤、胃肠系统等疾病；如果短时间内，体重急剧增长，一方面和你的不健康饮食有关，另一方面，也可能和高血脂、甲减、糖尿病有关。国内外大量研究显示，约有60%—80%的成年糖尿病患者在发病前体重超标。</p><p style=\"text-align: justify;\">主食和油</p><p style=\"text-align: justify;\">糖尿病人这样吃更安全</p><p style=\"text-align: justify;\">3.体温指标</p><p style=\"text-align: justify;\">正常人的体温应该为36℃～37℃，超过37℃就可以确诊为发烧。除了发烧外，还有一种情况，就是体温低于正常体温，称为“低体温”。“低体温”常出现在高龄老人，长期营养不足的患者身上，甲减或者时常休克的病人，也会有这种情况。</p><p style=\"text-align: justify;\">4.脉搏指标（心跳指标）</p><p style=\"text-align: justify;\">成人标准脉搏应该为每分钟60～100次（注：运动员的脉搏可能低于这个标准）。如果出现脉搏过速、过缓、有间歇、脉搏较弱、时快时慢，这均表示，可能心脏有问题，需要及时就医。老人心跳一般会略低于标准数，不过，只要能保持不低于55次/分钟，就算是正常的。如果平时心跳较慢，突然增至80～90次每分钟，就要考虑是不是得了潜在疾病，需要马上就医检查。</p><p style=\"text-align: justify;\">5.呼吸指标</p><p style=\"text-align: justify;\">健康人的呼吸应该是平稳，有规律的。每分钟16～18次左右。如果呼吸急促、大喘气、或者气不够用，时快时慢，胸闷，憋气等现象都是不正常的表现。呼吸急促、喘不过气多见于哮喘疾病；胸闷、憋气多见于心脏疾病。对于老人来说，心肺功能减弱，运动后也可能会有心悸气短的症状，不过，如果休息后，症状缓解，就是正常的，并不是疾病的表现。</p><p style=\"text-align: justify;\">6.排便指标</p><p style=\"text-align: justify;\">健康人的排便次数每天或者隔天一次。正常的大便应该是黄色软状。高龄老人，饮食少、运动少的，2～3天排便一次也是正常的。只要排便畅通，大便不干，就不是便秘。对于普通人来说，如果超过3天未排便，而且排便困难、排不尽、大便发干，这就是得了便秘；如果每天排便超过三次，并且大便不成形，便稀，这种情况一般就是得了腹泻了。结肠炎也可以通过大便检查出来。一般来说，患有结肠炎的病人，会有便血、便秘或者腹泻等症状。</p><p style=\"text-align: justify;\">7.排尿指标</p><p style=\"text-align: justify;\">成人的排尿量每天应该在1～2升左右，2～4小时就要排尿一次（夜间除外）。健康人的尿液应该是淡黄色，透明、少许泡沫。如果小便黄中带红，就要考虑尿路感染的情况；小便呈蓝绿色，多见于绿脓杆菌感染；血尿常见于泌尿生殖系统疾病、肿瘤或者结石等；尿频、尿急，这种情况就不用说了，是前列腺疾病的典型症状。</p><p style=\"text-align: justify;\">8.血压指标</p><p style=\"text-align: justify;\">这个大家应该都比较熟悉。成人的血压应该是不超过140/80毫米汞柱。对于老人来说，血管壁弹性降低，体内垃圾积累过多，需要心脏加大压力，才能保证正常的血氧供应，所以血压会上升。不过要注意，老人的收缩压不应超过160毫米汞柱，如果超过这个标准，就可以判定为高血压，不管有没有不舒服的症状都应吃药。如果单纯的是舒张压过高，需要去医院检查，切忌私自用药。</p><p style=\"text-align: justify;\"><img src=\"https://p3-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/T1cRrWvC8OWZ77~noop.image?_iz=58558&amp;from=article.pc_detail&amp;lk3s=953192f4&amp;x-expires=1721543150&amp;x-signature=%2F5yaAFAWB6ZB75WWQN%2BcrulPDns%3D\" alt=\"\" data-href=\"\" style=\"height: auto;\"></p><p style=\"text-align: justify;\">9.睡眠指标</p><p style=\"text-align: justify;\">一般来说，成人的睡眠时间应该在6～8小时，睡足8小时不是标准，而是应该以起床时精神状态是否饱满作为标准。而且每个年龄段的人群，睡眠时间是不一样的。10～18岁的人群，要保证每天8小时睡眠时间；18～50岁的人群，保证每天7小时睡眠即可；50～70岁，每天只需要5～6小时睡觉就够了。对于老人来说，睡眠质量会有所下降，所以不能硬性规定每天要睡多久。只要睡醒后，白天有精神，无疲劳感就可以。另外，建议老人要养成午休的习惯，有利于身体健康。</p><p style=\"text-align: justify;\">10.精神指标</p><p style=\"text-align: justify;\">世界卫生组织把人体精神健康的标准概括为“三良好”：</p><p style=\"text-align: justify;\">良好的个性人格——情绪稳定，性格温和，一直坚强，感情丰富，豁达乐观。</p><p style=\"text-align: justify;\">良好的处世能力——观察问题客观，有较强的自我控制能力，能适应复杂的社会环境。</p><p style=\"text-align: justify;\">良好的人际关系——待人接物大度和善，助人为乐，与人为善。</p><p style=\"text-align: justify;\">健康人应该有饱满的精神状态，丰富的情感、敏捷的行动能力。如果不具备这些以及上面的“三良好”，就需要考虑是不是身体有隐疾了。</p><p>大家快来对照看看自己的这些指标是否合格吧！有了健康上的小问题要及时发现治疗，否则可能形成大隐患！</p>', 2, 'http://localhost:8000/media/show/14.png', NULL, 1, '2024-07-14 14:27:51');
INSERT INTO `news` VALUES (4, '健康的7大准则，做到2个就很厉害', '<p>有人说，打败一个年轻人，只需要一张体检报告单。</p><p style=\"text-align: justify;\"><br></p><p style=\"text-align: justify;\">中年青年报社社会调查中心做过一项调查，45.2%的受访青年表示害怕参加体检，其中95后受访者表示害怕体检的比例最高，为52.3%。</p><p style=\"text-align: justify;\"><br></p><p style=\"text-align: justify;\">害怕体检，68.1%的受访者是担心会查出身体有问题。</p><p style=\"text-align: justify;\"><br></p><p style=\"text-align: justify;\"><strong>的确，不少疾病都在呈现年轻化的趋势，以前认为六七十岁才患的病，如今很多二三十岁的已经深受困扰。</strong></p><p style=\"text-align: justify;\"><br></p><p style=\"text-align: justify;\">比如骨质疏松、中风、二型糖尿病等等，一档关注认知障碍的电视节目《忘不了餐厅》，曾邀请过一位嘉宾，她在36岁时就确诊了阿尔茨海默病。</p><p style=\"text-align: justify;\"><br></p><p style=\"text-align: justify;\">如果说造成疾病的是不良的饮食习惯和结构、不规律的作息、缺乏运动等生活方式，那么，又是什么导致我们过上了这种带来疾病的生活方式？</p><p style=\"text-align: justify;\"><br></p><p style=\"text-align: justify;\">《运动改造大脑》的作者、哈佛医学院教授约翰·瑞迪，有一本书叫《医生最想让你做的事》。</p><p style=\"text-align: justify;\"><br></p><p style=\"text-align: justify;\">他指出，文明发展迅速，但我们的身体并没有跟上时代的步伐。这种失配影响到我们生活的每个领域，包括身体健康，还有情感健康。</p><p style=\"text-align: justify;\"><br></p><p style=\"text-align: justify;\"><strong>瑞迪教授认为，疾病不是源于人身体结构上的不足或缺陷，而是源于生活方式带来的自我损伤。</strong></p><p style=\"text-align: justify;\"><img src=\"https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/1ddd7fb50276407cb6f7c5f6cfefbf33~noop.image?_iz=58558&amp;from=article.pc_detail&amp;lk3s=953192f4&amp;x-expires=1721543305&amp;x-signature=yaW6sAE2E5qxjedMaYsFdnJiBI4%3D\" alt=\"\" data-href=\"\" style=\"height: auto;\"></p><p><br></p><p style=\"text-align: justify;\">人类在进化过程中，本身积累了三个核心优势，但是现代生活，让这些优势的作用正在渐渐失效。</p><p style=\"text-align: justify;\"><br></p><p style=\"text-align: justify;\"><strong>首先，人类在运动方面很全能。</strong></p><p style=\"text-align: justify;\"><br></p><p style=\"text-align: justify;\">猿类都能跑，但跑不快，也跑不远，但人类可以。</p><p style=\"text-align: justify;\"><br></p><p style=\"text-align: justify;\">跑的前提是直立行走，同时需要调动大脑来进行协调和规划，在运动方面，人类就是个全能选手。</p><p style=\"text-align: justify;\"><br></p><p style=\"text-align: justify;\">而今，很多人一坐就是几个小时，运动量只有从家到地铁站的步行距离。</p><p style=\"text-align: justify;\"><br></p><p style=\"text-align: justify;\"><strong>其次是人类饮食的多样化。</strong></p><p style=\"text-align: justify;\"><br></p><p style=\"text-align: justify;\">人是杂食动物，肠道中有成千上万种菌群，它们分解食物后给食物增加的价值也远远超过了我们的想象。</p><p style=\"text-align: justify;\">饮食多样性，能确保人类摄取种类足够多的微量营养素，以支撑复杂的人体运转。</p><p style=\"text-align: justify;\">但是今天的人类，食物中大量的是能快速提供能量的精加工制品，丧失了食物本身的完整性。</p><p style=\"text-align: justify;\"><img src=\"https://p3-sign.toutiaoimg.com/tos-cn-i-qvj2lq49k0/450f91c6160849e0ba8e2a07756f240f~noop.image?_iz=58558&amp;from=article.pc_detail&amp;lk3s=953192f4&amp;x-expires=1721543305&amp;x-signature=ooUPVyq%2FJJWHFdwakIVOjBT4uMw%3D\" alt=\"\" data-href=\"\" style=\"width: 50%;\"></p><p><br></p><p style=\"text-align: justify;\"><strong>最后，人类富有同理心。</strong></p><p style=\"text-align: justify;\"><br></p><p style=\"text-align: justify;\">20世纪八九十年代，意大利科学家团队发现了一种名为“镜像神经元”的细胞。</p><p style=\"text-align: justify;\"><br></p><p style=\"text-align: justify;\">研究人员在猴子吃花生时对其大脑进行监测，观察到一组神经元在放电。</p><p style=\"text-align: justify;\"><br></p><p style=\"text-align: justify;\">如果让一只猴子看另一只猴子吃花生，它脑内的同一组神经元也会放电，就好像它自己就是那只吃花生的猴子，那就是镜像神经元在放电。</p><p style=\"text-align: justify;\"><br></p><p style=\"text-align: justify;\">人不仅仅能察觉到他人的感受，甚至还会感同身受，这就是同理心。</p><p style=\"text-align: justify;\"><br></p><p style=\"text-align: justify;\">同理心是人类存在的基础，有同理心，人类才能凝聚在一起，才能合作。</p><p style=\"text-align: justify;\"><br></p><p style=\"text-align: justify;\">而今天的人，患上了社交恐惧症，不愿与人相处，更喜欢独自面对世界。</p><p style=\"text-align: justify;\"><br></p><p style=\"text-align: justify;\">比尔及梅琳达·盖茨基金会曾经进行过一项覆盖全世界187个国家的大规模研究，对死亡、身体虚弱及生活质量下降的成因进行了调查。</p><p style=\"text-align: justify;\"><br></p><p><strong>研究认为，全球范围内，造成疾病和身体虚弱的12个危险因素分别是：高血压、吸烟、酒精、油烟污染、水果摄入较少、体重指数高、高血糖、体重低、空气污染、缺乏活动、盐摄入量高、坚果和籽类食物摄入量低。</strong></p>', 1, 'http://localhost:8000/media/show/12.png', NULL, 1, '2024-07-14 14:29:09');
INSERT INTO `news` VALUES (5, '健康体重管理行动', '<p>一、行动背景</p> \r\n<p style=\"text-align: justify;\">    随着经济社会的发展，特别是人口老龄化，居民生产生活方式、饮食结构的变化，我国重大慢性病发展总体呈上升趋势，因慢性病导致的死亡人数比例已经超过80%，慢性病防控形势较为严峻。研究表明，体重水平与人体健康状况密切相关，体重异常特别是超重和肥胖是导致心脑血管疾病、糖尿病和部分癌症等慢性病的重要危险因素，已经成为威胁我国居民健康的重大公共卫生问题。</p><p style=\"text-align: justify;\">将健康体重管理纳入健康中国专项行动中予以积极推动和倡导，促进全民健康，既是普及健康生活方式，提高居民健康素养的需要，更是坚持预防为主，推动慢性病防控关口前移的必要举措。</p><p style=\"text-align: justify;\">    二、行动目标</p><p style=\"text-align: justify;\">明确了到2030年，实现体重管理支持性环境广泛建立，全民体重管理意识和技能显著提升，健康生活方式更加普及，全民参与、人人受益的体重管理良好局面基本形成，人群超重肥胖上升趋势初步减缓，部分人群体重异常状况得以改善。</p>\r\n<p style=\"text-align: justify;\">三、行动主要内容</p><p style=\"text-align: justify;\">（一）工作措施。围绕行动目标提出2个方面8条主要工作措施。在个人和家庭层面，提出要正确认识体重，科学管理体重，掌握体重管理技能。在社会和政府层面，提出加强科学普及和宣传倡导，发挥专业技术优势、规范体重管理服务模式，积极营造良好的体重管理社会支持性环境，倡导健康消费新理念，加强体重监测与效果评估等工作任务。</p>\r\n<p style=\"text-align: justify;\">（二）主要指标。围绕行动目标提出2个方面4个指标。在个人和社会方面，倡导个人掌握体重管理知识与技能，倡导家庭、医疗卫生机构、学校、机关企事业单位、宾馆等配置体重秤。在政府工作方面，要求编制和发布体重管理权威信息，倡导推动体重管理科普宣教进家庭、进社区、进医疗卫生机构、进机关企事业单位、进宾馆、进餐馆食堂等。</p>', 3, 'http://localhost:8000/media/show/11.png', NULL, 0, '2024-07-14 14:34:58');
INSERT INTO `news` VALUES (6, '睡眠质量对健康的影响及改善方法', '<p>30年前……</p><p style=\"text-align: justify;\">癌症和心脏病离我们很远</p><p style=\"text-align: justify;\">很少听说糖尿病</p><p style=\"text-align: justify;\">医学教科书里没有“脂肪肝”</p><p style=\"text-align: justify;\">极少有精神和心理疾病</p><p style=\"text-align: justify;\">很少有人喝奶和吃奶粉</p><p style=\"text-align: justify;\">从来没有听说过补钙</p><p style=\"text-align: justify;\">只有逢年过节才喝酒助兴</p><p style=\"text-align: justify;\">几乎看不到胖子</p><p style=\"text-align: left;\"><br></p><p style=\"text-align: justify;\">现在……</p><p style=\"text-align: justify;\">每5个人就有一个患慢性病</p><p style=\"text-align: justify;\">每年增加1200万慢性病人</p><p style=\"text-align: justify;\">每5个成年人就有一个心血管病</p><p style=\"text-align: justify;\">每10秒就有一人死于心血管疾病</p><p style=\"text-align: left;\"><br></p><p style=\"text-align: justify;\">现在……</p><p style=\"text-align: justify;\">肺癌死亡率增加了5倍</p><p style=\"text-align: justify;\">地球上每3个肺癌就有一个在中国</p><p style=\"text-align: justify;\">烟民人数世界第一</p><p style=\"text-align: justify;\">喝酒人数世界第一</p><p style=\"text-align: justify;\">精神和心理疾病人数世界排名第一</p><p style=\"text-align: justify;\">糖尿病人数世界排名第一</p><p style=\"text-align: justify;\">所以我们今天整理了一篇健康大数据数据，以下是各大年龄段的健康数据情况！</p><p style=\"text-align: justify;\"><br></p><p style=\"text-align: justify;\">中国人健康大数据概况</p><p style=\"text-align: justify;\">中国高血压人口有1.6——1.7亿人</p><p style=\"text-align: justify;\">高血脂的有将１亿多人</p><p style=\"text-align: justify;\">糖尿病患者达到9240万人</p><p style=\"text-align: justify;\">超重或者肥胖症7000万——２亿人</p><p style=\"text-align: justify;\">血脂异常的1.6亿人</p><p style=\"text-align: justify;\">脂肪肝患者约1.2２亿人</p><p style=\"text-align: justify;\">平均每30秒就有一个人罹患癌症</p><p style=\"text-align: justify;\">平均每30秒就有一个人罹患糖尿病</p><p style=\"text-align: justify;\">平均每30秒，至少有一个人死于心脑血管疾病</p><p style=\"text-align: justify;\">中国城市白领的健康堪忧</p><p style=\"text-align: justify;\">目前我国主流城市的白领亚健康比例高达76%，处于过劳状态的白领接近六成，<strong>真正意义上的健康人比例不足3%。</strong></p><p style=\"text-align: justify;\">白领女性更容易受到妇科、心脑血管疾病的威胁，男性则面临猝死、过劳、癌症等问题！</p><p style=\"text-align: justify;\">中国社科院《人才发展报告》：七种职业有过劳死的危险，如果中国知识分子不注意调整亚健康状态，不久的将来这些人中的2/3死于心脑血管疾病！</p><p style=\"text-align: justify;\"><img src=\"https://p3-sign.toutiaoimg.com/pgc-image/aa3e04dcf48349e290d9975aa17e431a~noop.image?_iz=58558&amp;from=article.pc_detail&amp;lk3s=953192f4&amp;x-expires=1721722113&amp;x-signature=wRHPZWa1UKZ7UI6UFFaakvp9Elk%3D\" alt=\"\" data-href=\"\" style=\"height: auto;\"></p><p><br></p><p style=\"text-align: justify;\">健康和医生治疗没有直接关系</p><p style=\"text-align: justify;\">美国研究证实：与美国人健康寿命相关的因素中，只有10%跟医疗相关！</p><p style=\"text-align: justify;\">导致美国人健康寿命延长30年中，有25年与医学没有关系。</p><p style=\"text-align: justify;\">普通疾病的误诊率高达27%左右，重大疾病的误诊率高达40%左右。</p><p style=\"text-align: justify;\">美国研究证实：高度发达的现代医学体系与人的健康没有太大关系。</p><p style=\"text-align: justify;\">英国研究证实：有85%的药品是无效的，对病人最好的措施就是尽量减少医疗干预。</p><p style=\"text-align: justify;\">美国研究证实：有30%——40%的手术根本不需要做！</p><p style=\"text-align: justify;\">药物的不良反应是对健康的重大威胁</p><p style=\"text-align: justify;\">《千手观音》23位主要演员中19位都是因药物不良反应导致聋哑。</p><p style=\"text-align: justify;\">著名的美国医学协会杂志（JAMA）曾经发布过一篇令人震惊的报告,在1994年因为严重的药物副作用而需要住院治疗的人数也超过了220万人。</p><p style=\"text-align: justify;\">更令人吃惊的是，这其中有超过10．6万人死于药物副作用。</p><p style=\"text-align: justify;\">这份报告在医学界一石激起千层浪。我们以前从不知道，会有如此之多的患者深受药物副作用的危害。</p><p style=\"text-align: justify;\">2006年9月12日是我国首个“预防出生缺陷日”，同年监测显示，我国每天有720个缺陷儿出生。其中很多是药物的不良反应造成的。</p><p style=\"text-align: justify;\"><br></p><p style=\"text-align: justify;\">第四次国家卫生服务调查结果显示</p><p style=\"text-align: justify;\">2008年，慢性病患病率就已达20%，死亡数已占总死亡数的83%。</p><p style=\"text-align: justify;\">过去十一年，平均每年新增慢性病例接近了２倍。心脏病和恶性肿瘤病例增加了近1倍！</p><p style=\"text-align: justify;\">美国《保健事物》杂志报告，中国人的腰围增长速度将成为世界之最。肥胖人口将达到3.25亿，未来20年将会增长一倍，腰围只要增长一英寸（2.54厘米），血管就会增长４英里，患癌风险高８倍！</p><p style=\"text-align: justify;\">中国青少年健康大数据</p><p style=\"text-align: justify;\">80%学生早餐营养质量较差</p><p style=\"text-align: justify;\">青春期贫血的发病率达38%</p><p style=\"text-align: justify;\">全国肥胖儿中脂肪肝发生率40—50%</p><p style=\"text-align: justify;\">小学生近视率32.5%</p><p style=\"text-align: justify;\">初中生59.4%</p><p style=\"text-align: justify;\">高中生77.3%</p><p>大学生80%</p>', 3, 'http://localhost:8000/media/show/6.png', NULL, 0, '2024-07-16 16:09:06');
INSERT INTO `news` VALUES (7, '快节奏的现代生活，如同一只无形的手', '<p> </p><p style=\"text-align: justify;\">在过去，随着中国经济的高速发展，许多人的生活水平和物质条件得到了很大的改善。然而，这种快速发展的背后，却隐藏着一些被忽视的问题，其中较为突出的就是健康问题。当经济增速放缓，社会逐渐趋向和谐时，人们开始意识到，健康才是生活中更为重要的一部分。</p><p style=\"text-align: justify;\"><strong>中国人的健康数据，触目惊心！</strong></p><p style=\"text-align: justify;\">经过精心搜集与整理，我们获得了一组关于中国人健康状况的详尽数据。它们不仅仅是冷冰冰的统计结果，更像是一个个鲜活的生命在向我们诉说着健康的宝贵。</p><p style=\"text-align: justify;\">高血压——1.6-1.7亿人</p><p style=\"text-align: justify;\">高血脂——1亿多人</p><p style=\"text-align: justify;\">糖尿病患者——9240万人</p><p style=\"text-align: justify;\">超重或者肥胖症——7000万-----2亿人</p><p style=\"text-align: justify;\">血脂异常——1.6亿人</p><p style=\"text-align: justify;\">脂肪肝患者——1.2亿人</p><p style=\"text-align: justify;\">平均每30秒，就有一个人罹患癌症，</p><p style=\"text-align: justify;\">平均每30秒，就有一个人罹患糖尿病，</p><p style=\"text-align: justify;\">平均每30秒，至少有一个人死于心脑血管疾病。</p><p style=\"text-align: justify;\">这些冰冷的数字背后，是无数家庭的痛苦和无奈。它们无声地诉说着一个残酷的真相：在繁忙的生活中，我们往往为了追逐金钱和物质享受，而忽略了身体的健康。当健康问题如暗流涌动，悄然而至时，我们才如梦初醒，惊觉已为时晚矣！</p><p style=\"text-align: justify;\"><strong>树立良好的健康理念</strong></p><p style=\"text-align: justify;\">快节奏的现代生活，如同一只无形的手，推动着我们不断前行，却也在不经意间，让我们生活方式和饮食习惯发生了很大的变化。作息不规律、高油高盐的饮食等，悄然侵蚀着我们的健康，使得慢性疾病的阴影逐渐笼罩在我们的生活之上。</p><p style=\"text-align: justify;\">更为严峻的是，我们对健康的重视程度仍然远远不够。在过去的日子里，人们紧紧盯着经济的发展和物质条件的改善，却忘记了健康才是生命的根基。我们需要的，不仅仅是医疗技术的日新月异，更需要的是健康理念的深入人心，健康行为的自觉养成。</p><p style=\"text-align: justify;\">健康对于每个人来说都是刻不容缓的。我们要珍惜自己的身体，我们要时刻提醒自己，健康才是重要的，不要等到失去健康之后才后悔莫及。 </p><p style=\"text-align: justify;\"><strong>补肽刻不容缓</strong></p><p style=\"text-align: justify;\">疾病，就像一位潜藏在暗处的狡猾猎手，随时准备向我们发动攻击。它的存在无声无息，却又无比强大，一旦被我们忽视，便有可能迅速蔓延，成为威胁我们生命安全的熊熊烈火。而补肽，这一健康管理的利器，正是我们对抗疾病、保持健康的重要武器。</p><p style=\"text-align: justify;\">补肽，顾名思义，就是补充身体所需的肽类物质。人体本身就含有小分子肽，但随着年龄的增长，肽类物质会逐渐减少，导致身体各项功能逐渐衰退。因此，及时补充肽类物质，对于保持身体健康具有重要意义。</p><p style=\"text-align: justify;\">小分子肽，如同一位贴心的守护者，为我们的身体健康筑起一道坚实的屏障，让我们在面对外界病邪时更有抵抗力，还能帮助身体更好地吸收营养，预防慢性疾病的发生。</p><p style=\"text-align: justify;\">记住，健康是我们宝贵的财富，只有拥有健康的身体，我们才能更好地享受生活、追求梦想。因为没有了健康，我们就无法享受生活的美好，无法陪伴家人，无法实现自己的梦想。</p><p>所以，为了自己，为了家人，为了亲朋，保健养生从现在做起！在这个充满挑战和机遇的时代里，让我们一起携手前行，用补肽这一健康管理利器守护我们的健康之路。</p>', 3, 'http://localhost:8000/media/show/7.jpg', NULL, NULL, '2024-07-16 16:10:35');
INSERT INTO `news` VALUES (8, '我们对健康的重视程度仍然远远不够', '<p> </p><p style=\"text-align: justify;\">在过去，随着中国经济的高速发展，许多人的生活水平和物质条件得到了很大的改善。然而，这种快速发展的背后，却隐藏着一些被忽视的问题，其中较为突出的就是健康问题。当经济增速放缓，社会逐渐趋向和谐时，人们开始意识到，健康才是生活中更为重要的一部分。</p><p style=\"text-align: justify;\"><strong>中国人的健康数据，触目惊心！</strong></p><p style=\"text-align: justify;\">经过精心搜集与整理，我们获得了一组关于中国人健康状况的详尽数据。它们不仅仅是冷冰冰的统计结果，更像是一个个鲜活的生命在向我们诉说着健康的宝贵。</p><p style=\"text-align: justify;\">高血压——1.6-1.7亿人</p><p style=\"text-align: justify;\">高血脂——1亿多人</p><p style=\"text-align: justify;\">糖尿病患者——9240万人</p><p style=\"text-align: justify;\">超重或者肥胖症——7000万-----2亿人</p><p style=\"text-align: justify;\">血脂异常——1.6亿人</p><p style=\"text-align: justify;\">脂肪肝患者——1.2亿人</p><p style=\"text-align: justify;\">平均每30秒，就有一个人罹患癌症，</p><p style=\"text-align: justify;\">平均每30秒，就有一个人罹患糖尿病，</p><p style=\"text-align: justify;\">平均每30秒，至少有一个人死于心脑血管疾病。</p><p style=\"text-align: justify;\">这些冰冷的数字背后，是无数家庭的痛苦和无奈。它们无声地诉说着一个残酷的真相：在繁忙的生活中，我们往往为了追逐金钱和物质享受，而忽略了身体的健康。当健康问题如暗流涌动，悄然而至时，我们才如梦初醒，惊觉已为时晚矣！</p><p style=\"text-align: justify;\"><strong>树立良好的健康理念</strong></p><p style=\"text-align: justify;\">快节奏的现代生活，如同一只无形的手，推动着我们不断前行，却也在不经意间，让我们生活方式和饮食习惯发生了很大的变化。作息不规律、高油高盐的饮食等，悄然侵蚀着我们的健康，使得慢性疾病的阴影逐渐笼罩在我们的生活之上。</p><p style=\"text-align: justify;\">更为严峻的是，我们对健康的重视程度仍然远远不够。在过去的日子里，人们紧紧盯着经济的发展和物质条件的改善，却忘记了健康才是生命的根基。我们需要的，不仅仅是医疗技术的日新月异，更需要的是健康理念的深入人心，健康行为的自觉养成。</p><p style=\"text-align: justify;\">健康对于每个人来说都是刻不容缓的。我们要珍惜自己的身体，我们要时刻提醒自己，健康才是重要的，不要等到失去健康之后才后悔莫及。 </p><p style=\"text-align: justify;\"><strong>补肽刻不容缓</strong></p><p style=\"text-align: justify;\">疾病，就像一位潜藏在暗处的狡猾猎手，随时准备向我们发动攻击。它的存在无声无息，却又无比强大，一旦被我们忽视，便有可能迅速蔓延，成为威胁我们生命安全的熊熊烈火。而补肽，这一健康管理的利器，正是我们对抗疾病、保持健康的重要武器。</p><p style=\"text-align: justify;\">补肽，顾名思义，就是补充身体所需的肽类物质。人体本身就含有小分子肽，但随着年龄的增长，肽类物质会逐渐减少，导致身体各项功能逐渐衰退。因此，及时补充肽类物质，对于保持身体健康具有重要意义。</p><p style=\"text-align: justify;\">小分子肽，如同一位贴心的守护者，为我们的身体健康筑起一道坚实的屏障，让我们在面对外界病邪时更有抵抗力，还能帮助身体更好地吸收营养，预防慢性疾病的发生。</p><p style=\"text-align: justify;\">记住，健康是我们宝贵的财富，只有拥有健康的身体，我们才能更好地享受生活、追求梦想。因为没有了健康，我们就无法享受生活的美好，无法陪伴家人，无法实现自己的梦想。</p><p>所以，为了自己，为了家人，为了亲朋，保健养生从现在做起！在这个充满挑战和机遇的时代里，让我们一起携手前行，用补肽这一健康管理利器守护我们的健康之路。</p>', 3, 'http://localhost:8000/media/show/8.jpg', NULL, NULL, '2024-07-16 16:11:31');
INSERT INTO `news` VALUES (9, '慢性疾病的阴影逐渐笼罩在我们的生活之上', '<p> </p><p style=\"text-align: justify;\">在过去，随着中国经济的高速发展，许多人的生活水平和物质条件得到了很大的改善。然而，这种快速发展的背后，却隐藏着一些被忽视的问题，其中较为突出的就是健康问题。当经济增速放缓，社会逐渐趋向和谐时，人们开始意识到，健康才是生活中更为重要的一部分。</p><p style=\"text-align: justify;\"><strong>中国人的健康数据，触目惊心！</strong></p><p style=\"text-align: justify;\">经过精心搜集与整理，我们获得了一组关于中国人健康状况的详尽数据。它们不仅仅是冷冰冰的统计结果，更像是一个个鲜活的生命在向我们诉说着健康的宝贵。</p><p style=\"text-align: justify;\">高血压——1.6-1.7亿人</p><p style=\"text-align: justify;\">高血脂——1亿多人</p><p style=\"text-align: justify;\">糖尿病患者——9240万人</p><p style=\"text-align: justify;\">超重或者肥胖症——7000万-----2亿人</p><p style=\"text-align: justify;\">血脂异常——1.6亿人</p><p style=\"text-align: justify;\">脂肪肝患者——1.2亿人</p><p style=\"text-align: justify;\">平均每30秒，就有一个人罹患癌症，</p><p style=\"text-align: justify;\">平均每30秒，就有一个人罹患糖尿病，</p><p style=\"text-align: justify;\">平均每30秒，至少有一个人死于心脑血管疾病。</p><p style=\"text-align: justify;\">这些冰冷的数字背后，是无数家庭的痛苦和无奈。它们无声地诉说着一个残酷的真相：在繁忙的生活中，我们往往为了追逐金钱和物质享受，而忽略了身体的健康。当健康问题如暗流涌动，悄然而至时，我们才如梦初醒，惊觉已为时晚矣！</p><p style=\"text-align: justify;\"><strong>树立良好的健康理念</strong></p><p style=\"text-align: justify;\">快节奏的现代生活，如同一只无形的手，推动着我们不断前行，却也在不经意间，让我们生活方式和饮食习惯发生了很大的变化。作息不规律、高油高盐的饮食等，悄然侵蚀着我们的健康，使得慢性疾病的阴影逐渐笼罩在我们的生活之上。</p><p style=\"text-align: justify;\">更为严峻的是，我们对健康的重视程度仍然远远不够。在过去的日子里，人们紧紧盯着经济的发展和物质条件的改善，却忘记了健康才是生命的根基。我们需要的，不仅仅是医疗技术的日新月异，更需要的是健康理念的深入人心，健康行为的自觉养成。</p><p style=\"text-align: justify;\">健康对于每个人来说都是刻不容缓的。我们要珍惜自己的身体，我们要时刻提醒自己，健康才是重要的，不要等到失去健康之后才后悔莫及。 </p><p style=\"text-align: justify;\"><strong>补肽刻不容缓</strong></p><p style=\"text-align: justify;\">疾病，就像一位潜藏在暗处的狡猾猎手，随时准备向我们发动攻击。它的存在无声无息，却又无比强大，一旦被我们忽视，便有可能迅速蔓延，成为威胁我们生命安全的熊熊烈火。而补肽，这一健康管理的利器，正是我们对抗疾病、保持健康的重要武器。</p><p style=\"text-align: justify;\">补肽，顾名思义，就是补充身体所需的肽类物质。人体本身就含有小分子肽，但随着年龄的增长，肽类物质会逐渐减少，导致身体各项功能逐渐衰退。因此，及时补充肽类物质，对于保持身体健康具有重要意义。</p><p style=\"text-align: justify;\">小分子肽，如同一位贴心的守护者，为我们的身体健康筑起一道坚实的屏障，让我们在面对外界病邪时更有抵抗力，还能帮助身体更好地吸收营养，预防慢性疾病的发生。</p><p style=\"text-align: justify;\">记住，健康是我们宝贵的财富，只有拥有健康的身体，我们才能更好地享受生活、追求梦想。因为没有了健康，我们就无法享受生活的美好，无法陪伴家人，无法实现自己的梦想。</p><p>所以，为了自己，为了家人，为了亲朋，保健养生从现在做起！在这个充满挑战和机遇的时代里，让我们一起携手前行，用补肽这一健康管理利器守护我们的健康之路。</p>', 2, 'http://localhost:8000/media/show/15.png', NULL, NULL, '2024-07-16 16:12:23');
INSERT INTO `news` VALUES (10, '如何建立健康的生活方式：有效的健康管理技巧', '<p> </p><p style=\"text-align: justify;\">在过去，随着中国经济的高速发展，许多人的生活水平和物质条件得到了很大的改善。然而，这种快速发展的背后，却隐藏着一些被忽视的问题，其中较为突出的就是健康问题。当经济增速放缓，社会逐渐趋向和谐时，人们开始意识到，健康才是生活中更为重要的一部分。</p><p style=\"text-align: justify;\"><strong>中国人的健康数据，触目惊心！</strong></p><p style=\"text-align: justify;\">经过精心搜集与整理，我们获得了一组关于中国人健康状况的详尽数据。它们不仅仅是冷冰冰的统计结果，更像是一个个鲜活的生命在向我们诉说着健康的宝贵。</p><p style=\"text-align: justify;\">高血压——1.6-1.7亿人</p><p style=\"text-align: justify;\">高血脂——1亿多人</p><p style=\"text-align: justify;\">糖尿病患者——9240万人</p><p style=\"text-align: justify;\">超重或者肥胖症——7000万-----2亿人</p><p style=\"text-align: justify;\">血脂异常——1.6亿人</p><p style=\"text-align: justify;\">脂肪肝患者——1.2亿人</p><p style=\"text-align: justify;\">平均每30秒，就有一个人罹患癌症，</p><p style=\"text-align: justify;\">平均每30秒，就有一个人罹患糖尿病，</p><p style=\"text-align: justify;\">平均每30秒，至少有一个人死于心脑血管疾病。</p><p style=\"text-align: justify;\">这些冰冷的数字背后，是无数家庭的痛苦和无奈。它们无声地诉说着一个残酷的真相：在繁忙的生活中，我们往往为了追逐金钱和物质享受，而忽略了身体的健康。当健康问题如暗流涌动，悄然而至时，我们才如梦初醒，惊觉已为时晚矣！</p><p style=\"text-align: justify;\"><strong>树立良好的健康理念</strong></p><p style=\"text-align: justify;\">快节奏的现代生活，如同一只无形的手，推动着我们不断前行，却也在不经意间，让我们生活方式和饮食习惯发生了很大的变化。作息不规律、高油高盐的饮食等，悄然侵蚀着我们的健康，使得慢性疾病的阴影逐渐笼罩在我们的生活之上。</p><p style=\"text-align: justify;\">更为严峻的是，我们对健康的重视程度仍然远远不够。在过去的日子里，人们紧紧盯着经济的发展和物质条件的改善，却忘记了健康才是生命的根基。我们需要的，不仅仅是医疗技术的日新月异，更需要的是健康理念的深入人心，健康行为的自觉养成。</p><p style=\"text-align: justify;\">健康对于每个人来说都是刻不容缓的。我们要珍惜自己的身体，我们要时刻提醒自己，健康才是重要的，不要等到失去健康之后才后悔莫及。 </p><p style=\"text-align: justify;\"><strong>补肽刻不容缓</strong></p><p style=\"text-align: justify;\">疾病，就像一位潜藏在暗处的狡猾猎手，随时准备向我们发动攻击。它的存在无声无息，却又无比强大，一旦被我们忽视，便有可能迅速蔓延，成为威胁我们生命安全的熊熊烈火。而补肽，这一健康管理的利器，正是我们对抗疾病、保持健康的重要武器。</p><p style=\"text-align: justify;\">补肽，顾名思义，就是补充身体所需的肽类物质。人体本身就含有小分子肽，但随着年龄的增长，肽类物质会逐渐减少，导致身体各项功能逐渐衰退。因此，及时补充肽类物质，对于保持身体健康具有重要意义。</p><p style=\"text-align: justify;\">小分子肽，如同一位贴心的守护者，为我们的身体健康筑起一道坚实的屏障，让我们在面对外界病邪时更有抵抗力，还能帮助身体更好地吸收营养，预防慢性疾病的发生。</p><p style=\"text-align: justify;\">记住，健康是我们宝贵的财富，只有拥有健康的身体，我们才能更好地享受生活、追求梦想。因为没有了健康，我们就无法享受生活的美好，无法陪伴家人，无法实现自己的梦想。</p><p>所以，为了自己，为了家人，为了亲朋，保健养生从现在做起！在这个充满挑战和机遇的时代里，让我们一起携手前行，用补肽这一健康管理利器守护我们的健康之路。</p>', 3, 'http://localhost:8000/media/show/5.jpg', NULL, 0, '2024-07-16 16:12:56');
INSERT INTO `news` VALUES (11, '为了家人，为了亲朋，保健养生从现在做起！', '<p> 在过去，随着中国经济的高速发展，许多人的生活水平和物质条件得到了很大的改善。然而，这种快速发展的背后，却隐藏着一些被忽视的问题，其中较为突出的就是健康问题。当经济增速放缓，社会逐渐趋向和谐时，人们开始意识到，健康才是生活中更为重要的一部分。</p><p style=\"text-align: justify;\"><strong>中国人的健康数据，触目惊心！</strong></p><p style=\"text-align: justify;\">经过精心搜集与整理，我们获得了一组关于中国人健康状况的详尽数据。它们不仅仅是冷冰冰的统计结果，更像是一个个鲜活的生命在向我们诉说着健康的宝贵。</p><p style=\"text-align: justify;\">高血压——1.6-1.7亿人</p><p style=\"text-align: justify;\">高血脂——1亿多人</p><p style=\"text-align: justify;\">糖尿病患者——9240万人</p><p style=\"text-align: justify;\">超重或者肥胖症——7000万-----2亿人</p><p style=\"text-align: justify;\">血脂异常——1.6亿人</p><p style=\"text-align: justify;\">脂肪肝患者——1.2亿人</p><p style=\"text-align: justify;\">平均每30秒，就有一个人罹患癌症，</p><p style=\"text-align: justify;\">平均每30秒，就有一个人罹患糖尿病，</p><p style=\"text-align: justify;\">平均每30秒，至少有一个人死于心脑血管疾病。</p><p style=\"text-align: justify;\">这些冰冷的数字背后，是无数家庭的痛苦和无奈。它们无声地诉说着一个残酷的真相：在繁忙的生活中，我们往往为了追逐金钱和物质享受，而忽略了身体的健康。当健康问题如暗流涌动，悄然而至时，我们才如梦初醒，惊觉已为时晚矣！</p><p style=\"text-align: justify;\"><strong>树立良好的健康理念</strong></p><p style=\"text-align: justify;\">快节奏的现代生活，如同一只无形的手，推动着我们不断前行，却也在不经意间，让我们生活方式和饮食习惯发生了很大的变化。作息不规律、高油高盐的饮食等，悄然侵蚀着我们的健康，使得慢性疾病的阴影逐渐笼罩在我们的生活之上。</p><p style=\"text-align: justify;\">更为严峻的是，我们对健康的重视程度仍然远远不够。在过去的日子里，人们紧紧盯着经济的发展和物质条件的改善，却忘记了健康才是生命的根基。我们需要的，不仅仅是医疗技术的日新月异，更需要的是健康理念的深入人心，健康行为的自觉养成。</p><p style=\"text-align: justify;\">健康对于每个人来说都是刻不容缓的。我们要珍惜自己的身体，我们要时刻提醒自己，健康才是重要的，不要等到失去健康之后才后悔莫及。 </p><p style=\"text-align: justify;\"><strong>补肽刻不容缓</strong></p><p style=\"text-align: justify;\">疾病，就像一位潜藏在暗处的狡猾猎手，随时准备向我们发动攻击。它的存在无声无息，却又无比强大，一旦被我们忽视，便有可能迅速蔓延，成为威胁我们生命安全的熊熊烈火。而补肽，这一健康管理的利器，正是我们对抗疾病、保持健康的重要武器。</p><p style=\"text-align: justify;\">补肽，顾名思义，就是补充身体所需的肽类物质。人体本身就含有小分子肽，但随着年龄的增长，肽类物质会逐渐减少，导致身体各项功能逐渐衰退。因此，及时补充肽类物质，对于保持身体健康具有重要意义。</p><p style=\"text-align: justify;\">小分子肽，如同一位贴心的守护者，为我们的身体健康筑起一道坚实的屏障，让我们在面对外界病邪时更有抵抗力，还能帮助身体更好地吸收营养，预防慢性疾病的发生。</p><p style=\"text-align: justify;\">记住，健康是我们宝贵的财富，只有拥有健康的身体，我们才能更好地享受生活、追求梦想。因为没有了健康，我们就无法享受生活的美好，无法陪伴家人，无法实现自己的梦想。</p><p style=\"text-align: justify;\">所以，为了自己，为了家人，为了亲朋，保健养生从现在做起！在这个充满挑战和机遇的时代里，让我们一起携手前行，用补肽这一健康管理利器守护我们的健康之路。</p>', 2, 'http://localhost:8000/media/show/5.jpg\r\n', NULL, 0, '2024-07-16 16:13:40');
INSERT INTO `news` VALUES (12, '探讨健康饮食对身体的重要性', '<p> 在过去，随着中国经济的高速发展，许多人的生活水平和物质条件得到了很大的改善。然而，这种快速发展的背后，却隐藏着一些被忽视的问题，其中较为突出的就是健康问题。当经济增速放缓，社会逐渐趋向和谐时，人们开始意识到，健康才是生活中更为重要的一部分。</p><p><br></p><p style=\"text-align: justify;\"><strong>中国人的健康数据，触目惊心！</strong></p><p style=\"text-align: justify;\">经过精心搜集与整理，我们获得了一组关于中国人健康状况的详尽数据。它们不仅仅是冷冰冰的统计结果，更像是一个个鲜活的生命在向我们诉说着健康的宝贵。</p><p style=\"text-align: justify;\">高血压——1.6-1.7亿人</p><p style=\"text-align: justify;\">高血脂——1亿多人</p><p style=\"text-align: justify;\">糖尿病患者——9240万人</p><p style=\"text-align: justify;\">超重或者肥胖症——7000万-----2亿人</p><p style=\"text-align: justify;\">血脂异常——1.6亿人</p><p style=\"text-align: justify;\">脂肪肝患者——1.2亿人</p><p style=\"text-align: justify;\">平均每30秒，就有一个人罹患癌症，</p><p style=\"text-align: justify;\">平均每30秒，就有一个人罹患糖尿病，</p><p style=\"text-align: justify;\">平均每30秒，至少有一个人死于心脑血管疾病。</p><p style=\"text-align: justify;\">这些冰冷的数字背后，是无数家庭的痛苦和无奈。它们无声地诉说着一个残酷的真相：在繁忙的生活中，我们往往为了追逐金钱和物质享受，而忽略了身体的健康。当健康问题如暗流涌动，悄然而至时，我们才如梦初醒，惊觉已为时晚矣！</p><p style=\"text-align: justify;\"><strong>树立良好的健康理念</strong></p><p style=\"text-align: justify;\">快节奏的现代生活，如同一只无形的手，推动着我们不断前行，却也在不经意间，让我们生活方式和饮食习惯发生了很大的变化。作息不规律、高油高盐的饮食等，悄然侵蚀着我们的健康，使得慢性疾病的阴影逐渐笼罩在我们的生活之上。</p><p style=\"text-align: justify;\">更为严峻的是，我们对健康的重视程度仍然远远不够。在过去的日子里，人们紧紧盯着经济的发展和物质条件的改善，却忘记了健康才是生命的根基。我们需要的，不仅仅是医疗技术的日新月异，更需要的是健康理念的深入人心，健康行为的自觉养成。</p><p style=\"text-align: justify;\">健康对于每个人来说都是刻不容缓的。我们要珍惜自己的身体，我们要时刻提醒自己，健康才是重要的，不要等到失去健康之后才后悔莫及。 </p><p style=\"text-align: justify;\"><strong>补肽刻不容缓</strong></p><p style=\"text-align: justify;\">疾病，就像一位潜藏在暗处的狡猾猎手，随时准备向我们发动攻击。它的存在无声无息，却又无比强大，一旦被我们忽视，便有可能迅速蔓延，成为威胁我们生命安全的熊熊烈火。而补肽，这一健康管理的利器，正是我们对抗疾病、保持健康的重要武器。</p><p style=\"text-align: justify;\">补肽，顾名思义，就是补充身体所需的肽类物质。人体本身就含有小分子肽，但随着年龄的增长，肽类物质会逐渐减少，导致身体各项功能逐渐衰退。因此，及时补充肽类物质，对于保持身体健康具有重要意义。</p><p style=\"text-align: justify;\">小分子肽，如同一位贴心的守护者，为我们的身体健康筑起一道坚实的屏障，让我们在面对外界病邪时更有抵抗力，还能帮助身体更好地吸收营养，预防慢性疾病的发生。</p><p style=\"text-align: justify;\">记住，健康是我们宝贵的财富，只有拥有健康的身体，我们才能更好地享受生活、追求梦想。因为没有了健康，我们就无法享受生活的美好，无法陪伴家人，无法实现自己的梦想。</p><p style=\"text-align: justify;\">所以，为了自己，为了家人，为了亲朋，保健养生从现在做起！在这个充满挑战和机遇的时代里，让我们一起携手前行，用补肽这一健康管理利器守护我们的健康之路。</p>', 1, 'http://localhost:8000/media/show/5.jpg', NULL, 1, '2024-07-16 16:14:27');

-- ----------------------------
-- Table structure for sys_menu
-- ----------------------------
DROP TABLE IF EXISTS `sys_menu`;
CREATE TABLE `sys_menu`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `icon` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL,
  `parent_id` int NULL DEFAULT NULL,
  `order_num` int NULL DEFAULT NULL,
  `path` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL,
  `component` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL,
  `menu_type` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL,
  `perms` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL,
  `create_time` date NULL DEFAULT NULL,
  `update_time` date NULL DEFAULT NULL,
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sys_menu
-- ----------------------------
INSERT INTO `sys_menu` VALUES (1, '系统管理', 'system', 0, 1, '/sys', '', 'M', '', '2024-07-04', '2024-07-04', '系统管理目录');
INSERT INTO `sys_menu` VALUES (2, '待开发...', 'monitor', 0, 2, '/bsns', '', 'M', '', '2024-07-04', '2024-07-04', '业务管理目录');
INSERT INTO `sys_menu` VALUES (3, '用户管理', 'user', 1, 1, '/sys/user', 'sys/user/index', 'C', 'system:user:list', '2024-07-04', '2024-07-04', '用户管理菜单');
INSERT INTO `sys_menu` VALUES (4, '评论管理', 'peoples', 1, 2, '/sys/role', 'sys/role/index', 'C', 'system:role:list', '2024-07-04', '2024-07-04', '角色管理菜单');
INSERT INTO `sys_menu` VALUES (5, '待开发', 'tree table', 1, 3, '/sys/menu', 'sys/menu/index', 'C', 'system:menu:list', '2024-07-04', '2024-07-04', '菜单管理菜单');
INSERT INTO `sys_menu` VALUES (6, '部门管理', 'tree', 2, 1, '/bsns/department', 'bsns/Department', 'C', '', '2024-07-04', '2024-07-04', '部门管理菜单');
INSERT INTO `sys_menu` VALUES (7, '岗位管理', 'post', 2, 2, '/bsns/post', 'bsns/Post', 'C', '', '2024-07-04', '2024-07-04', '岗位管理菜单');

-- ----------------------------
-- Table structure for sys_role
-- ----------------------------
DROP TABLE IF EXISTS `sys_role`;
CREATE TABLE `sys_role`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL,
  `code` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL,
  `create_time` date NULL DEFAULT NULL,
  `update_time` date NULL DEFAULT NULL,
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 23 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sys_role
-- ----------------------------
INSERT INTO `sys_role` VALUES (1, '超级管理员', 'admin', '2024-07-04', '2024-07-04', '拥有系统最高权限');
INSERT INTO `sys_role` VALUES (2, '普通角色', 'common', '2024-07-04', '2024-07-04', '普通角色');
INSERT INTO `sys_role` VALUES (3, '测试角色', 'test', '2024-07-04', '2024-07-04', '测试角色');
INSERT INTO `sys_role` VALUES (4, '是', NULL, '2024-07-04', '2024-07-04', NULL);
INSERT INTO `sys_role` VALUES (5, '3', NULL, '2024-07-04', '2024-07-04', NULL);
INSERT INTO `sys_role` VALUES (6, '4', NULL, '2024-07-04', '2024-07-04', NULL);
INSERT INTO `sys_role` VALUES (19, '测2', 'cc2', '2024-07-04', '2024-07-04', 'eewew2');
INSERT INTO `sys_role` VALUES (20, 'ccc测试', 'test2', '2024-07-04', '2024-07-04', 'xxx');
INSERT INTO `sys_role` VALUES (21, '今天测试角色', 'todytest', '2024-07-04', '2024-07-04', 'ccc');
INSERT INTO `sys_role` VALUES (22, '12', '123', '2024-07-04', '2024-08-29', '12');

-- ----------------------------
-- Table structure for sys_role_menu
-- ----------------------------
DROP TABLE IF EXISTS `sys_role_menu`;
CREATE TABLE `sys_role_menu`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `menu_id` int NOT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `sys_role_menu_menu_id_5c7ca896_fk_sys_menu_id`(`menu_id` ASC) USING BTREE,
  INDEX `sys_role_menu_role_id_e0dcb43b_fk_sys_role_id`(`role_id` ASC) USING BTREE,
  CONSTRAINT `sys_role_menu_menu_id_5c7ca896_fk_sys_menu_id` FOREIGN KEY (`menu_id`) REFERENCES `sys_menu` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `sys_role_menu_role_id_e0dcb43b_fk_sys_role_id` FOREIGN KEY (`role_id`) REFERENCES `sys_role` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 119 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sys_role_menu
-- ----------------------------
INSERT INTO `sys_role_menu` VALUES (102, 2, 2);
INSERT INTO `sys_role_menu` VALUES (103, 6, 2);
INSERT INTO `sys_role_menu` VALUES (104, 7, 2);
INSERT INTO `sys_role_menu` VALUES (106, 1, 1);
INSERT INTO `sys_role_menu` VALUES (107, 3, 1);
INSERT INTO `sys_role_menu` VALUES (108, 4, 1);
INSERT INTO `sys_role_menu` VALUES (109, 5, 1);
INSERT INTO `sys_role_menu` VALUES (110, 2, 1);
INSERT INTO `sys_role_menu` VALUES (111, 6, 1);
INSERT INTO `sys_role_menu` VALUES (112, 7, 1);
INSERT INTO `sys_role_menu` VALUES (114, 1, 6);
INSERT INTO `sys_role_menu` VALUES (115, 5, 6);
INSERT INTO `sys_role_menu` VALUES (116, 2, 6);
INSERT INTO `sys_role_menu` VALUES (117, 6, 6);
INSERT INTO `sys_role_menu` VALUES (118, 7, 6);

-- ----------------------------
-- Table structure for sys_user
-- ----------------------------
DROP TABLE IF EXISTS `sys_user`;
CREATE TABLE `sys_user`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL,
  `phonenumber` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL,
  `login_date` date NULL DEFAULT NULL,
  `status` int NULL DEFAULT NULL,
  `create_time` date NULL DEFAULT NULL,
  `update_time` date NULL DEFAULT NULL,
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 32 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_bin ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sys_user
-- ----------------------------
INSERT INTO `sys_user` VALUES (1, '你看看', 'pbkdf2_sha256$390000$8bRqeUnEtIFJtMO00mSxwf$7kzBt/Xb5xyaQ4b5N6kZvBQDsMabX85rejVOONConPs=', '20250318121701.jpg', 'caofeng2015@126.com', '18862857108', '2024-08-08', 1, '2024-08-08', '2025-03-18', '超级管理员');
INSERT INTO `sys_user` VALUES (3, '1', 'pbkdf2_sha256$600000$cHKXCKm1aqG4GtT64gIoWf$zfYxXsoqjlZg9DLR+cwILFwsO/mzvyEYWRHkZMcf9Ts=', '20240808230603.jpg', 'caofeng2014@126.com', '18862857104', '2024-08-08', 0, '2024-08-08', '2025-03-18', '测试用户3.18');
INSERT INTO `sys_user` VALUES (6, '4', 'pbkdf2_sha256$600000$myyo3yISRGQclhcSEAHfmB$Zg3TnnablQriQG1B97RBewf4r+eiYHMx1IeImVEJCAM=', '20240808230603.jpg', NULL, NULL, NULL, 0, NULL, NULL, NULL);
INSERT INTO `sys_user` VALUES (7, '5', 'pbkdf2_sha256$600000$ug2Kn90rh77VvpCFnrXawD$lXxmxwxGrM2NBU+9aHbB4tw35OcmbN14HW6/2nlwq04=', '20240808230603.jpg', NULL, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO `sys_user` VALUES (11, '9', 'pbkdf2_sha256$600000$qHh68A8Don5YTLehB5qJgo$wO9Y7RQCvUCMG41legbg3vogAQQ78w9du3yIiq0a/+4=', '20240808230603.jpg', NULL, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO `sys_user` VALUES (14, '666', 'pbkdf2_sha256$600000$cExYmEFz2ljgeqFcySIeul$AxWN9NaIRTReL1FzHtJ5RrRrcheBvGD743yRmDCEG4Y=', 'default.jpg', 'caofeng2014@126.com', '18862857104', NULL, 1, '2024-08-13', NULL, '33');
INSERT INTO `sys_user` VALUES (15, 'jack', 'pbkdf2_sha256$600000$gwTajosBuqDWwlf6sxqIQX$JfqkhVdp41KXfnk7wVrENgeAz1f2197MXpLdIDmvX4M=', 'default.jpg', 'caofeng2014@126.com', '18862857104', NULL, 1, '2024-08-13', '2024-09-06', '禁用用户测试4');
INSERT INTO `sys_user` VALUES (16, '12323232', 'pbkdf2_sha256$600000$cTxMe5ynlQY5Vu2VhcyR0N$4SKA1VIvLdARG+HtbJvIqdjYST1c2QwJIu0lxpB2GTg=', 'default.jpg', '1@126.com', '18862857104', NULL, 1, '2024-08-18', '2024-08-18', '115');
INSERT INTO `sys_user` VALUES (17, 'marry', 'pbkdf2_sha256$600000$RKyUZxWhXhSOPPkuCzO6jo$KN7+ARTLD8U4MK+cZfliI+UA3hpczQksEnHfVxhoel0=', 'default.jpg', '111@qq.com', '15586521012', NULL, 1, '2024-09-05', NULL, '555');
INSERT INTO `sys_user` VALUES (18, 'testuser', 'pbkdf2_sha256$600000$yBh5vZt7cDHg4KnChFVAvD$QkmkCxBjkzKKW0Jb2Ykh3DWhdQtMWbF1yH6OPF2GBNI=', NULL, 'test@example.com', '13812345678', NULL, 0, '2025-03-04', NULL, NULL);
INSERT INTO `sys_user` VALUES (19, '2819153126', 'pbkdf2_sha256$600000$56vW2Sfayqi5q3rLlTAFqL$gKHt9baZvpsjyYMVEyZFqI6l79FgXF07IrdBTh00YWg=', NULL, 'test1@qq.com', '13717328036', NULL, 0, '2025-03-04', NULL, NULL);
INSERT INTO `sys_user` VALUES (20, '111111111', 'pbkdf2_sha256$600000$ov0v7YYEYLUzwHlfMrhDlR$MzcOdkpAjdUGPUTxp4DGNATfE7xPW67pM30zO1mfCW4=', NULL, 'test01@qq.com', '17363826382', NULL, 0, '2025-03-04', NULL, NULL);
INSERT INTO `sys_user` VALUES (21, 'test02', 'pbkdf2_sha256$600000$MM25QJ6BsM1QcpSoDPZIU5$mZ3KDRrORtStEu14xg0aJUZP1moTuS8pG133D8aT3tU=', NULL, 'test02@qq.com', '18264765789', NULL, 0, '2025-03-04', NULL, NULL);
INSERT INTO `sys_user` VALUES (22, 'test03', 'pbkdf2_sha256$600000$RH85gaRHHz56LEdjbDMJqJ$vPfd8WYdHPNoRZ+1dema5BCpc0GA8wKc1Yc+An0gwtM=', 'blob:http://localhost:8080/f89e0c75-ebb4-4768-8afc-78299ef3844a', 'test03@qq.com', '13725647898', NULL, 0, '2025-03-04', '2025-03-18', NULL);
INSERT INTO `sys_user` VALUES (23, 'test04', 'pbkdf2_sha256$600000$S5hDsyMzfKsLMEI1yBHuK1$Y0A9/PtkRvWSiUdVfEnwO4+7ubSo1VMnLLJC5ZXJtls=', NULL, 'test04@qq.com', '18765378903', NULL, 1, '2025-03-18', NULL, NULL);
INSERT INTO `sys_user` VALUES (24, 'test05', 'pbkdf2_sha256$600000$9YkAk8V9H5o9L0CFsn0omp$hRRNrfGQBJ99JB7CDY7mmEgbJy6F8aoA1IYx4CrS4c4=', NULL, 'test05@qq.com', '18398907645', NULL, 0, '2025-03-18', NULL, NULL);
INSERT INTO `sys_user` VALUES (25, 'test06', 'pbkdf2_sha256$600000$Yi3RPFy2s9PN5HRDXjUbgL$G/6inU+AfSjg++/JmSePOWsDgrXosd2gPUNstndBkxg=', NULL, 'test@qq.com', '18635426745', NULL, 0, '2025-03-18', NULL, NULL);
INSERT INTO `sys_user` VALUES (26, 'test07', 'pbkdf2_sha256$600000$8yT6nfIfDPN4BcgwokmvNx$UxuCz5kF91fJm/ulZrkN/heoDOLA6f8jAtz4NZiIjCo=', NULL, 'test07@qq.com', '15678945345', NULL, 0, '2025-03-18', NULL, NULL);
INSERT INTO `sys_user` VALUES (27, 'test08', 'pbkdf2_sha256$600000$botzO0TMJCJqgqehguFQBX$nsSia1HgaL9Wii/u7lTPICJfUa2yaS0hU3cpI58lD20=', NULL, 'test08@qq.com', '18256435685', NULL, 0, '2025-03-18', NULL, NULL);
INSERT INTO `sys_user` VALUES (28, 'test09', 'pbkdf2_sha256$600000$otBnbfSYTO1WqT8DH6WVQw$tYQ/+XGnl0p4sd1eZZg+uUCMjiLVze/4ccfPMlFrG/I=', NULL, NULL, NULL, NULL, 1, '2025-03-18', NULL, NULL);
INSERT INTO `sys_user` VALUES (29, 'test10', 'pbkdf2_sha256$600000$swCi39hqcdfU4dyznIDI94$+Gik+ocwY9ob3fOaUKVH8avmvd5ASrgrBdopKvr8K04=', NULL, 'test10@qq.com', '18356274567', NULL, 1, '2025-03-18', NULL, NULL);
INSERT INTO `sys_user` VALUES (30, 'kkn', 'pbkdf2_sha256$390000$MQvwtVhwTNYk1RQ5C9dgaw$2/lz+xEtLNVP5hpFpXTTTc1W1iI67eh6hGLhWB77qvY=', NULL, '2075069454@qq.com', '18577888830', NULL, 1, '2025-04-25', NULL, NULL);
INSERT INTO `sys_user` VALUES (31, '饭了吗', 'pbkdf2_sha256$600000$RR1B9xeCvnx7FgiYkRj5ny$GqpKgTWj638NfvCwK3Ds01SYCgbxygo9mRH3y0GMTQI=', NULL, '5561165@qq.com', '13364485223', NULL, 1, '2025-05-06', NULL, NULL);

-- ----------------------------
-- Table structure for sys_user_role
-- ----------------------------
DROP TABLE IF EXISTS `sys_user_role`;
CREATE TABLE `sys_user_role`  (
  `id` int NOT NULL,
  `role_id` int NULL DEFAULT NULL,
  `user_id` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of sys_user_role
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;
