/*
 Navicat MySQL Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80018
 Source Host           : localhost:3306
 Source Schema         : mybbs

 Target Server Type    : MySQL
 Target Server Version : 80018
 File Encoding         : 65001

 Date: 27/09/2020 19:38:32
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version`  (
  `version_num` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`version_num`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for block
-- ----------------------------
DROP TABLE IF EXISTS `block`;
CREATE TABLE `block`  (
  `blockid` int(11) NOT NULL AUTO_INCREMENT,
  `blockname` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `plscount` int(11) NOT NULL,
  `tzscount` int(11) NOT NULL,
  `urlfor` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `urlfor1` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`blockid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for pinglun
-- ----------------------------
DROP TABLE IF EXISTS `pinglun`;
CREATE TABLE `pinglun`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `pinglunup` int(11) NOT NULL,
  `pinglundown` int(11) NOT NULL,
  `zhutieid` int(11) NULL DEFAULT NULL,
  `userid` int(11) NULL DEFAULT NULL,
  `pingluntime` date NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `userid`(`userid`) USING BTREE,
  INDEX `zhutieid`(`zhutieid`) USING BTREE,
  CONSTRAINT `pinglun_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `user` (`userid`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `pinglun_ibfk_2` FOREIGN KEY (`zhutieid`) REFERENCES `zhutie` (`zhutieid`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `userid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `tel` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gender` varchar(10) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `age` int(11) NULL DEFAULT NULL,
  `registerTime` date NOT NULL,
  `userlimit` int(11) NOT NULL,
  `email` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `touxiang` int(11) NOT NULL,
  PRIMARY KEY (`userid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for zhutie
-- ----------------------------
DROP TABLE IF EXISTS `zhutie`;
CREATE TABLE `zhutie`  (
  `zhutieid` int(11) NOT NULL AUTO_INCREMENT,
  `zhutietitle` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `zhutievalue` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `zhutielimit` int(11) NOT NULL,
  `zhutieup` int(11) NOT NULL,
  `userid` int(11) NULL DEFAULT NULL,
  `blockid` int(11) NULL DEFAULT NULL,
  `zhutieTime` date NULL DEFAULT NULL,
  PRIMARY KEY (`zhutieid`) USING BTREE,
  INDEX `userid`(`userid`) USING BTREE,
  INDEX `blockid`(`blockid`) USING BTREE,
  CONSTRAINT `zhutie_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `user` (`userid`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `zhutie_ibfk_2` FOREIGN KEY (`blockid`) REFERENCES `block` (`blockid`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 31 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Function structure for bkcounttz
-- ----------------------------
DROP FUNCTION IF EXISTS `bkcounttz`;
delimiter ;;
CREATE FUNCTION `bkcounttz`(`bk_id` int(255))
 RETURNS int(255)
  DETERMINISTIC
BEGIN
	DECLARE tzs int(255);
	SELECT COUNT(`zhutieid`) INTO tzs FROM `zhutie`
	WHERE blockid =bk_id;
	RETURN tzs;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for bkid2name
-- ----------------------------
DROP FUNCTION IF EXISTS `bkid2name`;
delimiter ;;
CREATE FUNCTION `bkid2name`(`bkid` varchar(50))
 RETURNS varchar(100) CHARSET utf8
  DETERMINISTIC
BEGIN
  DECLARE bkname VARCHAR(100);
	SELECT urlfor1 INTO bkname FROM `block`
	WHERE blockid = bkid;
	RETURN bkname;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for bkurlsearchbid
-- ----------------------------
DROP FUNCTION IF EXISTS `bkurlsearchbid`;
delimiter ;;
CREATE FUNCTION `bkurlsearchbid`(`url` varchar(500))
 RETURNS varchar(50) CHARSET utf8
  DETERMINISTIC
BEGIN
  DECLARE bkid VARCHAR(50);
	SELECT blockid INTO bkid FROM `block`
	WHERE  urlfor1 = url;
	RETURN bkid;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for countbk
-- ----------------------------
DROP FUNCTION IF EXISTS `countbk`;
delimiter ;;
CREATE FUNCTION `countbk`()
 RETURNS int(11)
  DETERMINISTIC
BEGIN
	DECLARE bks int(11);
	SELECT COUNT(`blockid`) INTO bks FROM `block`;
	RETURN bks;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for countpl
-- ----------------------------
DROP FUNCTION IF EXISTS `countpl`;
delimiter ;;
CREATE FUNCTION `countpl`(bk_id int(11))
 RETURNS int(11)
  DETERMINISTIC
BEGIN
	DECLARE pls int(11);
	SELECT COUNT(`id`)  INTO pls FROM `pinglun`,`zhutie`
	WHERE pinglun.zhutieid=zhutie.zhutieid and blockid=bk_id;
	RETURN pls;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for dh2id
-- ----------------------------
DROP FUNCTION IF EXISTS `dh2id`;
delimiter ;;
CREATE FUNCTION `dh2id`(`dh` varchar(50))
 RETURNS varchar(50) CHARSET utf8
  DETERMINISTIC
BEGIN
  DECLARE id VARCHAR(50);
	SELECT userid INTO id FROM `user`
	WHERE tel = dh ;
	RETURN id;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for plid2zhutieid
-- ----------------------------
DROP FUNCTION IF EXISTS `plid2zhutieid`;
delimiter ;;
CREATE FUNCTION `plid2zhutieid`(`plid` varchar(50))
 RETURNS varchar(50) CHARSET utf8
  DETERMINISTIC
BEGIN
  DECLARE ztid VARCHAR(50);
	SELECT zhutieid INTO ztid FROM `pinglun`
	WHERE id=plid;
	RETURN ztid;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for searchpl
-- ----------------------------
DROP FUNCTION IF EXISTS `searchpl`;
delimiter ;;
CREATE FUNCTION `searchpl`(`pl` varchar(500))
 RETURNS int(255)
  DETERMINISTIC
BEGIN
  DECLARE pl_id int(255);
	SELECT pinglunid INTO pl_id FROM `pinglun`
	WHERE pinglunvalue LIKE CONCAT('%',pl,'%') ;
	RETURN pl_id;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for searchtz
-- ----------------------------
DROP PROCEDURE IF EXISTS `searchtz`;
delimiter ;;
CREATE PROCEDURE `searchtz`(IN `tz` varchar(50))
BEGIN
	SELECT zhutieid FROM `zhutie`
	WHERE zhutietitle LIKE CONCAT('%',tz,'%') OR zhutievalue LIKE CONCAT('%',tz,'%') ;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for searchyh
-- ----------------------------
DROP FUNCTION IF EXISTS `searchyh`;
delimiter ;;
CREATE FUNCTION `searchyh`(`yh` varchar(50))
 RETURNS int(255)
  DETERMINISTIC
BEGIN
  DECLARE yh_id int(255);
	SELECT userid INTO yh_id FROM `user`
	WHERE username LIKE CONCAT('%',yh,'%') OR userid LIKE CONCAT('%',yh,'%');
	RETURN yh_id;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for tel2id
-- ----------------------------
DROP FUNCTION IF EXISTS `tel2id`;
delimiter ;;
CREATE FUNCTION `tel2id`(`usertel` varchar(50))
 RETURNS varchar(50) CHARSET utf8
  DETERMINISTIC
BEGIN
  DECLARE user_pw VARCHAR(50);
	SELECT `password` INTO user_pw FROM `user`
	WHERE tel = usertel ;
	RETURN user_pw;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for tel2limit
-- ----------------------------
DROP FUNCTION IF EXISTS `tel2limit`;
delimiter ;;
CREATE FUNCTION `tel2limit`(`usertel` varchar(50))
 RETURNS int(11)
  DETERMINISTIC
BEGIN
  DECLARE user_limit int(11);
	SELECT userlimit INTO user_limit FROM `user`
	WHERE tel = usertel ;
	RETURN user_limit;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for tel2pw
-- ----------------------------
DROP FUNCTION IF EXISTS `tel2pw`;
delimiter ;;
CREATE FUNCTION `tel2pw`(`usertel` varchar(50))
 RETURNS varchar(50) CHARSET utf8
  DETERMINISTIC
BEGIN
  DECLARE user_pw VARCHAR(50);
	SELECT `password` INTO user_pw FROM `user`
	WHERE tel = usertel ;
	RETURN user_pw;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for tzcountpl
-- ----------------------------
DROP FUNCTION IF EXISTS `tzcountpl`;
delimiter ;;
CREATE FUNCTION `tzcountpl`(`tz_id` int(255))
 RETURNS varchar(50) CHARSET utf8
  DETERMINISTIC
BEGIN
	DECLARE pls VARCHAR(50);
	SELECT COUNT(`id`) INTO pls FROM `pinglun`
	WHERE zhutieid =tz_id;
	RETURN pls;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for tzdetail
-- ----------------------------
DROP PROCEDURE IF EXISTS `tzdetail`;
delimiter ;;
CREATE PROCEDURE `tzdetail`(IN `tzid` int)
BEGIN
	SELECT * FROM zhutie
	WHERE zhutieid=tzid;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for tzid2block
-- ----------------------------
DROP FUNCTION IF EXISTS `tzid2block`;
delimiter ;;
CREATE FUNCTION `tzid2block`(`id` varchar(50))
 RETURNS int(11)
  DETERMINISTIC
BEGIN
  DECLARE block_id int(11);
	SELECT blockid INTO block_id FROM `zhutie`
	WHERE zhutieid = id ;
	RETURN block_id;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for tzid2limit
-- ----------------------------
DROP FUNCTION IF EXISTS `tzid2limit`;
delimiter ;;
CREATE FUNCTION `tzid2limit`(`id` varchar(50))
 RETURNS int(11)
  DETERMINISTIC
BEGIN
  DECLARE tz_limit int(11);
	SELECT zhutielimit INTO tz_limit FROM `zhutie`
	WHERE zhutieid = id ;
	RETURN tz_limit;
END
;;
delimiter ;

-- ----------------------------
-- Function structure for tzid2userid
-- ----------------------------
DROP FUNCTION IF EXISTS `tzid2userid`;
delimiter ;;
CREATE FUNCTION `tzid2userid`(`id` varchar(50))
 RETURNS varchar(50) CHARSET utf8
  DETERMINISTIC
BEGIN
  DECLARE uid VARCHAR(50);
	SELECT userid INTO uid FROM `zhutie`
	WHERE zhutieid = id ;
	RETURN uid;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table pinglun
-- ----------------------------
DROP TRIGGER IF EXISTS `Insert_pl_time`;
delimiter ;;
CREATE TRIGGER `Insert_pl_time` BEFORE INSERT ON `pinglun` FOR EACH ROW SET NEW.pinglunTime=(SELECT FROM_UNIXTIME(unix_timestamp(now()), '%Y-%m-%d %H:%i:%S'))
;
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table user
-- ----------------------------
DROP TRIGGER IF EXISTS `Insert_yh_time`;
delimiter ;;
CREATE TRIGGER `Insert_yh_time` BEFORE INSERT ON `user` FOR EACH ROW SET NEW.registerTime=(SELECT FROM_UNIXTIME(unix_timestamp(now()), '%Y-%m-%d'))
;
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table zhutie
-- ----------------------------
DROP TRIGGER IF EXISTS `Insert_tz_time`;
delimiter ;;
CREATE TRIGGER `Insert_tz_time` BEFORE INSERT ON `zhutie` FOR EACH ROW SET NEW.zhutieTime=(SELECT FROM_UNIXTIME(unix_timestamp(now()), '%Y-%m-%d'))
;
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table zhutie
-- ----------------------------
DROP TRIGGER IF EXISTS `updatebk`;
delimiter ;;
CREATE TRIGGER `updatebk` AFTER INSERT ON `zhutie` FOR EACH ROW BEGIN
SET @id=NEW.blockid;
SET @bkcount=(SELECT bkcounttz(@id));
UPDATE block SET block.tzscount=@bkcount WHERE block.blockid=@id;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table zhutie
-- ----------------------------
DROP TRIGGER IF EXISTS `updatebk_d`;
delimiter ;;
CREATE TRIGGER `updatebk_d` AFTER DELETE ON `zhutie` FOR EACH ROW BEGIN
SET @id=OLD.blockid;
SET @bkcount=(SELECT bkcounttz(@id));
UPDATE block SET block.tzscount=@bkcount WHERE block.blockid=@id;
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
