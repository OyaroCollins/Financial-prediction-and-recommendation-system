-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: smartfinance_db
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add budget',7,'add_budget'),(26,'Can change budget',7,'change_budget'),(27,'Can delete budget',7,'delete_budget'),(28,'Can view budget',7,'view_budget'),(29,'Can add category',8,'add_category'),(30,'Can change category',8,'change_category'),(31,'Can delete category',8,'delete_category'),(32,'Can view category',8,'view_category'),(33,'Can add transaction',9,'add_transaction'),(34,'Can change transaction',9,'change_transaction'),(35,'Can delete transaction',9,'delete_transaction'),(36,'Can view transaction',9,'view_transaction');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$600000$G2O7rPELcHpqDAHAWDzxrV$3yB+ddMTb307MZ1POUDSPG3TxO+T3myPJfLEF7RjSCg=','2026-09-12 03:04:07.549377',1,'collo','','','oyarocollins18@gmail.com',1,1,'2026-08-20 18:54:13.355366'),(2,'pbkdf2_sha256$600000$kIxjQXyI2cCAid2nF6i7q8$zpbNBR6zhS3mP4c+fZnHYyrJ/wBIZupbioGUi9XKNMM=','2026-09-12 14:58:03.160153',0,'_lumieregems','Lumiere','Gems','lumieregemsandjewel@gmail.com',0,1,'2026-08-21 11:22:03.517453'),(3,'pbkdf2_sha256$600000$LHaE5F8UY2dW0xqQJGFfDV$WJh5i11rczKj2WRj9Q3aOsUtRSYFbAIxdglFDtj1ebA=','2026-08-21 16:17:21.574002',0,'_afyabora','AfyaBora','Pharmacy','afyabora@gmail.com',0,1,'2026-08-21 16:17:20.998027');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session'),(7,'tracker','budget'),(8,'tracker','category'),(9,'tracker','transaction');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-08-20 18:51:48.849249'),(2,'auth','0001_initial','2026-08-20 18:51:50.225884'),(3,'admin','0001_initial','2026-08-20 18:51:50.526162'),(4,'admin','0002_logentry_remove_auto_add','2026-08-20 18:51:50.547131'),(5,'admin','0003_logentry_add_action_flag_choices','2026-08-20 18:51:50.567174'),(6,'contenttypes','0002_remove_content_type_name','2026-08-20 18:51:50.823674'),(7,'auth','0002_alter_permission_name_max_length','2026-08-20 18:51:50.984097'),(8,'auth','0003_alter_user_email_max_length','2026-08-20 18:51:51.037994'),(9,'auth','0004_alter_user_username_opts','2026-08-20 18:51:51.057805'),(10,'auth','0005_alter_user_last_login_null','2026-08-20 18:51:51.197210'),(11,'auth','0006_require_contenttypes_0002','2026-08-20 18:51:51.206867'),(12,'auth','0007_alter_validators_add_error_messages','2026-08-20 18:51:51.223953'),(13,'auth','0008_alter_user_username_max_length','2026-08-20 18:51:51.378632'),(14,'auth','0009_alter_user_last_name_max_length','2026-08-20 18:51:51.529029'),(15,'auth','0010_alter_group_name_max_length','2026-08-20 18:51:51.579985'),(16,'auth','0011_update_proxy_permissions','2026-08-20 18:51:51.598168'),(17,'auth','0012_alter_user_first_name_max_length','2026-08-20 18:51:51.750208'),(18,'sessions','0001_initial','2026-08-20 18:51:51.821899'),(19,'tracker','0001_initial','2026-08-21 10:40:37.759508');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('4db5bg58kp2h62qs1yi8zhs0v4nddd8j','.eJxVjDsOwyAQRO9CHSFg-YiU6XMGBMs6OIlAMnZl5e7BkoukmeLNm9lZiNtawtZpCXNmV6bY5ZeliC-qR5GfsT4ax1bXZU78UPjZdn5vmd630_07KLGXsY7aAZAhDygpCSu9mbJQLjmnSPkBtBVqJHpJg4MAmKxPmC1oI5F9vrkCNnY:1x5PB5:7D7T1nXz3RqkNVhE10JegjVeWWWW17MS4WpmUws3cOY','2026-09-26 14:58:03.178504'),('dc15n63kn71uu16omejttbnig1he153l','.eJxVjMsKwyAQAP9lz0XU1RVz7L3fID42NW1RiMmp9N9LIIf2OjPMG0Lctxr2wWtYCkyg4fLLUsxPbocoj9juXeTetnVJ4kjEaYe49cKv69n-DWocFSaIxiGyZY9ZcZKkvJ2L1C45p1l7ScqQ1KRM9oqldigRZ_IpF0JjVYbPF7kCNnY:1wzf0w:XVO35NT1Vr2DLzUBp6RuTptfVS8R_jzo6HaFPI9-yz4','2026-09-10 18:39:50.293919');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tracker_budget`
--

DROP TABLE IF EXISTS `tracker_budget`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tracker_budget` (
  `budget_id` int NOT NULL AUTO_INCREMENT,
  `amount` decimal(10,2) NOT NULL,
  `month` varchar(7) COLLATE utf8mb4_unicode_ci NOT NULL,
  `category_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`budget_id`),
  KEY `tracker_budget_category_id_9063dc9d_fk_tracker_c` (`category_id`),
  KEY `tracker_budget_user_id_7987a501_fk_auth_user_id` (`user_id`),
  CONSTRAINT `tracker_budget_category_id_9063dc9d_fk_tracker_c` FOREIGN KEY (`category_id`) REFERENCES `tracker_category` (`category_id`),
  CONSTRAINT `tracker_budget_user_id_7987a501_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tracker_budget`
--

LOCK TABLES `tracker_budget` WRITE;
/*!40000 ALTER TABLE `tracker_budget` DISABLE KEYS */;
INSERT INTO `tracker_budget` VALUES (1,800.00,'2026-08',5,2),(3,5000.00,'2026-09',3,2);
/*!40000 ALTER TABLE `tracker_budget` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tracker_category`
--

DROP TABLE IF EXISTS `tracker_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tracker_category` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`category_id`),
  KEY `tracker_category_user_id_edf2a226_fk_auth_user_id` (`user_id`),
  CONSTRAINT `tracker_category_user_id_edf2a226_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tracker_category`
--

LOCK TABLES `tracker_category` WRITE;
/*!40000 ALTER TABLE `tracker_category` DISABLE KEYS */;
INSERT INTO `tracker_category` VALUES (1,'Sales','Income',2),(3,'Stock','Expense',2),(5,'Transport','Expense',2),(6,'Meeting','Expense',2),(7,'Lunch','Expense',2),(8,'Tithe','Expense',2),(9,'Debts disbursed','Expense',2),(10,'Savings','Expense',2);
/*!40000 ALTER TABLE `tracker_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tracker_transaction`
--

DROP TABLE IF EXISTS `tracker_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tracker_transaction` (
  `transaction_id` int NOT NULL AUTO_INCREMENT,
  `amount` decimal(10,2) NOT NULL,
  `date` date NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `type` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `category_id` int NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`transaction_id`),
  KEY `tracker_transaction_category_id_21c6bddc_fk_tracker_c` (`category_id`),
  KEY `tracker_transaction_user_id_dabe7424_fk_auth_user_id` (`user_id`),
  CONSTRAINT `tracker_transaction_category_id_21c6bddc_fk_tracker_c` FOREIGN KEY (`category_id`) REFERENCES `tracker_category` (`category_id`),
  CONSTRAINT `tracker_transaction_user_id_dabe7424_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=104 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tracker_transaction`
--

LOCK TABLES `tracker_transaction` WRITE;
/*!40000 ALTER TABLE `tracker_transaction` DISABLE KEYS */;
INSERT INTO `tracker_transaction` VALUES (1,1900.00,'2026-01-10','January week 1','Income',1,2),(2,1050.00,'2026-01-15','January week 2','Income',1,2),(3,1245.00,'2026-01-24','January week 3','Income',1,2),(4,1250.00,'2026-01-31','January week 4','Income',1,2),(5,1050.00,'2026-01-12','January week 1','Expense',3,2),(6,850.00,'2026-01-17','January week 2\r\n','Expense',3,2),(7,800.00,'2026-01-26','January week 3','Expense',3,2),(8,970.00,'2026-02-02','Feb week 1\r\n','Expense',3,2),(9,3120.00,'2026-02-07','Feb week 1','Income',1,2),(10,2000.00,'2026-02-03','Feb week 1','Expense',3,2),(11,170.00,'2026-02-03','','Expense',5,2),(12,430.00,'2026-02-10','','Expense',5,2),(13,7010.00,'2026-02-14','Valentines week','Income',1,2),(14,4000.00,'2026-02-16','','Expense',3,2),(15,4712.00,'2026-02-21','','Income',1,2),(16,3500.00,'2026-02-23','','Expense',3,2),(17,1860.00,'2026-02-28','','Income',1,2),(18,1980.00,'2026-03-06','','Income',1,2),(19,1100.00,'2026-03-08','','Expense',3,2),(20,2890.00,'2026-03-14','','Income',1,2),(21,300.00,'2026-03-13','','Expense',5,2),(22,1700.00,'2026-03-16','','Expense',3,2),(23,3280.00,'2026-05-21','','Income',1,2),(24,410.00,'2026-03-18','','Expense',5,2),(25,1239.82,'2026-03-23','','Expense',3,2),(26,3130.00,'2026-03-28','','Income',1,2),(27,1800.00,'2026-03-30','','Expense',3,2),(31,3675.00,'2026-04-03','April week one','Income',1,2),(32,1370.00,'2026-04-06','','Expense',3,2),(33,7210.00,'2026-04-11','','Income',1,2),(34,3200.00,'2026-04-13','','Expense',3,2),(35,250.00,'2026-04-13','','Expense',5,2),(36,2920.00,'2026-04-18','','Income',1,2),(37,1584.93,'2026-04-20','','Expense',3,2),(38,4560.00,'2026-04-25','','Income',1,2),(39,2109.91,'2026-04-12','','Expense',3,2),(40,4080.00,'2026-05-02','May week 1','Income',1,2),(41,2499.92,'2026-05-04','','Expense',3,2),(42,2359.93,'2026-05-09','','Income',1,2),(43,2330.00,'2026-05-16','','Income',1,2),(44,1114.93,'2026-05-16','','Expense',3,2),(45,999.93,'2026-05-23','','Income',1,2),(46,2810.00,'2026-05-30','','Income',1,2),(47,280.00,'2026-05-30','A meeting was held on this day','Expense',6,2),(48,150.00,'2026-05-27','Lunch for staff meeting\r\n','Expense',7,2),(49,357.00,'2026-05-31','','Expense',8,2),(50,875.00,'2026-06-12','June week one','Income',1,2),(51,930.00,'2026-06-15','','Expense',3,2),(52,200.00,'2026-06-10','','Expense',7,2),(53,86.93,'2026-06-14','','Expense',8,2),(54,250.00,'2026-06-13','','Expense',9,2),(55,3600.00,'2026-06-27','','Income',1,2),(56,2600.00,'2026-06-28','','Expense',3,2),(57,160.00,'2026-06-26','','Expense',7,2),(58,215.00,'2026-06-27','','Expense',8,2),(59,2500.00,'2026-06-02','','Income',1,2),(60,1830.00,'2026-06-05','','Income',1,2),(61,3000.00,'2026-07-06','','Expense',3,2),(62,180.00,'2026-07-04','','Expense',7,2),(63,1850.00,'2026-07-11','July Week 1\r\n','Income',1,2),(64,1170.00,'2026-07-07','','Expense',3,2),(65,100.00,'2026-07-09','','Expense',7,2),(66,118.00,'2026-06-13','','Expense',8,2),(67,2510.00,'2026-07-18','','Income',1,2),(68,932.64,'2026-07-18','','Expense',3,2),(69,30.00,'2026-07-18','','Expense',7,2),(70,145.00,'2026-07-19','','Expense',8,2),(71,2060.00,'2026-07-25','','Income',1,2),(72,1022.73,'2026-07-22','','Expense',3,2),(73,134.85,'2026-07-26','','Expense',8,2),(74,2755.00,'2026-08-08','','Income',1,2),(75,549.79,'2026-08-08','','Income',1,2),(76,1123.00,'2026-08-04','','Expense',3,2),(77,257.00,'2026-08-09','','Expense',3,2),(78,160.00,'2026-08-05','','Expense',5,2),(79,198.00,'2026-08-09','','Expense',8,2),(80,2370.00,'2026-08-15','','Income',1,2),(81,970.00,'2026-08-15','','Expense',3,2),(82,80.00,'2026-08-13','Sweets','Expense',3,2),(83,413.00,'2026-08-15','','Expense',10,2),(84,2470.00,'2026-08-22','','Income',1,2),(85,2108.00,'2026-08-19','','Expense',3,2),(86,80.00,'2026-08-18','Sweets','Expense',3,2),(87,210.00,'2026-08-19','','Expense',5,2),(88,458.00,'2026-08-23','','Expense',8,2),(89,490.00,'2026-08-22','','Expense',10,2),(90,3060.00,'2026-08-29','Last week of August\r\n','Income',1,2),(91,1280.00,'2026-08-26','','Expense',3,2),(92,20.00,'2026-08-27','','Expense',7,2),(93,80.00,'2026-08-27','Sweets','Expense',3,2),(94,180.00,'2026-08-19','','Expense',5,2),(95,428.00,'2026-08-30','','Expense',8,2),(96,614.00,'2026-08-30','','Expense',10,2),(97,2490.00,'2026-09-05','Week one September','Income',1,2),(98,320.00,'2026-09-01','A meeting was held','Expense',6,2),(99,560.00,'2026-09-05','','Expense',9,2),(100,180.00,'2026-09-02','','Expense',5,2),(101,306.00,'2026-09-06','','Expense',8,2),(102,460.00,'2026-09-06','','Expense',10,2),(103,4550.00,'2026-09-14','I added some Necklaces','Expense',3,2);
/*!40000 ALTER TABLE `tracker_transaction` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-25  1:43:26
