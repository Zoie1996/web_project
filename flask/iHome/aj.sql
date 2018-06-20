/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50715
 Source Host           : localhost:3306
 Source Schema         : aj

 Target Server Type    : MySQL
 Target Server Version : 50715
 File Encoding         : 65001

 Date: 20/06/2018 16:27:29
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for home_facility
-- ----------------------------
DROP TABLE IF EXISTS `home_facility`;
CREATE TABLE `home_facility` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `css` varchar(30) DEFAULT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for ihome_area
-- ----------------------------
DROP TABLE IF EXISTS `ihome_area`;
CREATE TABLE `ihome_area` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ihome_area
-- ----------------------------
BEGIN;
INSERT INTO `ihome_area` VALUES (NULL, NULL, 1, '锦江区');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 2, '金牛区');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 3, '青羊区');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 4, '高新区');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 5, '武侯区');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 6, '天府新区');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 7, '双流县');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 8, '成华区');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 9, '青白江区');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 10, '新都区');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 11, '温江区');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 12, '温江区');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 13, '郫县');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 14, '蒲江县');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 15, '大邑县');
INSERT INTO `ihome_area` VALUES (NULL, NULL, 16, '新津县');
COMMIT;

-- ----------------------------
-- Table structure for ihome_facility
-- ----------------------------
DROP TABLE IF EXISTS `ihome_facility`;
CREATE TABLE `ihome_facility` (
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `css` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ihome_facility
-- ----------------------------
BEGIN;
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 1, '无线网络', 'wirelessnetwork-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 2, '热水淋浴', 'shower-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 3, '空调', 'aircondition-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 4, '暖气', 'heater-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 5, '允许吸烟', 'smoke-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 6, '饮水设备', 'drinking-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 7, '牙具', 'brush-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 8, '香皂', 'soap-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 9, '拖鞋', 'slippers-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 10, '手纸', 'toiletpaper-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 11, '毛巾', 'towel-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 12, '沐浴露、洗发露', 'toiletries-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 13, '冰箱', 'icebox-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 14, '洗衣机', 'washer-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 15, '电梯', 'elevator-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 16, '允许做饭', 'iscook-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 17, '允许带宠物', 'pet-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 18, '允许聚会', 'meet-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 19, '门禁系统', 'accesssys-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 20, '停车位', 'parkingspace-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 21, '有线网络', 'wirednetwork-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 22, '电视', 'tv-ico');
INSERT INTO `ihome_facility` VALUES (NULL, NULL, 23, '浴缸', 'jinzhi-ico');
COMMIT;

-- ----------------------------
-- Table structure for ihome_house
-- ----------------------------
DROP TABLE IF EXISTS `ihome_house`;
CREATE TABLE `ihome_house` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `area_id` int(11) DEFAULT NULL,
  `title` varchar(64) NOT NULL,
  `price` int(11) NOT NULL DEFAULT '0',
  `address` varchar(512) DEFAULT '',
  `room_count` int(11) DEFAULT '1',
  `acreage` int(11) DEFAULT '0',
  `unit` varchar(32) DEFAULT '',
  `capacity` int(11) DEFAULT '1',
  `beds` varchar(64) DEFAULT '',
  `deposit` int(11) DEFAULT '0',
  `min_days` int(11) DEFAULT '1',
  `max_days` int(11) DEFAULT '0',
  `order_count` int(11) DEFAULT '0',
  `index_image_url` varchar(256) DEFAULT '',
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_house_userid` (`user_id`),
  KEY `fk_house_araeid` (`area_id`),
  CONSTRAINT `fk_house_araeid` FOREIGN KEY (`area_id`) REFERENCES `ihome_area` (`id`),
  CONSTRAINT `fk_house_userid` FOREIGN KEY (`user_id`) REFERENCES `ihome_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for ihome_house_facility
-- ----------------------------
DROP TABLE IF EXISTS `ihome_house_facility`;
CREATE TABLE `ihome_house_facility` (
  `house_id` int(11) NOT NULL,
  `facility_id` int(11) NOT NULL,
  PRIMARY KEY (`house_id`,`facility_id`),
  KEY `fk_facility_araeid` (`facility_id`),
  CONSTRAINT `fk_facility_araeid` FOREIGN KEY (`facility_id`) REFERENCES `ihome_facility` (`id`),
  CONSTRAINT `fk_facility_houseid` FOREIGN KEY (`house_id`) REFERENCES `ihome_house` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for ihome_house_image
-- ----------------------------
DROP TABLE IF EXISTS `ihome_house_image`;
CREATE TABLE `ihome_house_image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `house_id` int(11) NOT NULL,
  `url` varchar(256) NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_image_houseid` (`house_id`),
  CONSTRAINT `fk_image_houseid` FOREIGN KEY (`house_id`) REFERENCES `ihome_house` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for ihome_order
-- ----------------------------
DROP TABLE IF EXISTS `ihome_order`;
CREATE TABLE `ihome_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `house_id` int(11) NOT NULL,
  `begin_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  `days` int(11) NOT NULL,
  `house_price` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  `status` enum('WAIT_ACCEPT','WAIT_PAYMENT','PAID','WAIT_COMMENT','COMPLETE','CANCELED','REJECTED') DEFAULT 'WAIT_ACCEPT',
  `comment` text,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for ihome_user
-- ----------------------------
DROP TABLE IF EXISTS `ihome_user`;
CREATE TABLE `ihome_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `phone` varchar(11) NOT NULL,
  `pwd_hash` varchar(200) NOT NULL,
  `name` varchar(30) DEFAULT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `id_name` varchar(30) DEFAULT NULL,
  `id_card` varchar(18) DEFAULT NULL,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `id_card` (`id_card`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ihome_user
-- ----------------------------
BEGIN;
INSERT INTO `ihome_user` VALUES (1, '13511112222', 'pbkdf2:sha256:50000$F5m9EBub$df085adeed7d629bf459ec2806fbff21d22a5fd2fe33e0eb3b79af2f49884f86', '来贸购', 'upload/IMG_0170.JPG', 'dama', '123456789012345678', '2018-06-19 14:30:03.451121', '2018-06-20 14:34:36.974092');
INSERT INTO `ihome_user` VALUES (2, '13511112223', 'pbkdf2:sha256:50000$aENDzLZG$139f976c6c691d9544d352e7b7c35499c17a930bed477553fd9a835d04c112cf', '来贸', 'upload/IMG_1086.JPG', NULL, NULL, '2018-06-19 14:34:24.898499', '2018-06-20 10:19:00.509905');
INSERT INTO `ihome_user` VALUES (3, '13511112224', 'pbkdf2:sha256:50000$fR46XKDO$8dcce6f8cb8e73b4bce1d9fdc5cddec272a35124812caa6f28878f69340dd686', '13511112224', NULL, NULL, NULL, '2018-06-19 14:44:35.113564', '2018-06-19 14:44:35.113723');
INSERT INTO `ihome_user` VALUES (4, '13511112225', 'pbkdf2:sha256:50000$eRuxr7ri$b0e7684cae1eeb359c8dbc9cd2e9e8d519655f6811c7d24e52683382b77c7c18', '13511112225', NULL, NULL, NULL, '2018-06-19 14:50:08.328342', '2018-06-19 14:50:08.329024');
INSERT INTO `ihome_user` VALUES (5, '13512341212', 'pbkdf2:sha256:50000$xix04XWa$4b5b84bd04b45f616e8b8f41a92095a4956de85c5495d0c408298bab0c3d9e0d', '13512341212', NULL, NULL, NULL, '2018-06-19 14:51:53.073858', '2018-06-19 14:51:53.074690');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
