# Creates test_db tables for using SeleniumBase with MySQL

# test_run_data table
# -----------------------------------
CREATE TABLE `test_run_data` (
  `guid` varchar(64) NOT NULL DEFAULT '',
  `test_address` varchar(255) DEFAULT NULL,
  `env` varchar(64) DEFAULT NULL,
  `start_time` varchar(64) DEFAULT NULL,
  `execution_guid` varchar(64) DEFAULT NULL,
  `runtime` int(11),
  `state` varchar(64) DEFAULT NULL,
  `browser` varchar(64) DEFAULT NULL,
  `message` text,
  `stack_trace` text,
  `retry_count` int(11) DEFAULT '0',
  `exception_map_guid` varchar(64) DEFAULT NULL,
  `log_url` text,
  PRIMARY KEY (`guid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

# execution table
# -----------------------------------
CREATE TABLE `execution` (
  `guid` varchar(64) NOT NULL DEFAULT '',
  `total_execution_time` int(11),
  `username` varchar(255) DEFAULT NULL,
  `execution_start` bigint(20) DEFAULT '0',
  PRIMARY KEY (`guid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

# delayed_test_data table
# -----------------------------------
CREATE TABLE `delayed_test_data` (
  `guid` varchar(64) NOT NULL DEFAULT '',
  `test_address` varchar(255) NOT NULL DEFAULT '',
  `inserted_at` bigint(20) NOT NULL,
  `expected_result` text,
  `is_done` tinyint(1) DEFAULT '0',
  `expires_at` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`guid`),
  UNIQUE KEY `uuid` (`guid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
