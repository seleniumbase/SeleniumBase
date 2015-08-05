# table delayedTestData
# -----------------------------------
CREATE TABLE `delayedTestData` (
  `guid` varchar(64) NOT NULL DEFAULT '',
  `testcaseAddress` varchar(255) NOT NULL DEFAULT '',
  `insertedAt` bigint(20) NOT NULL,
  `expectedResult` text,
  `done` tinyint(1) DEFAULT '0',
  `expiresAt` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`guid`),
  UNIQUE KEY `uuid` (`guid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

# table execution
# -----------------------------------
CREATE TABLE `execution` (
  `guid` varchar(64) NOT NULL DEFAULT '',
  `totalExecutionTime` int(11),
  `username` varchar(255) DEFAULT NULL,
  `executionStart` bigint(20) DEFAULT '0',
  PRIMARY KEY (`guid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

# table testcaseRunData
# -----------------------------------
CREATE TABLE `testcaseRunData` (
  `guid` varchar(64) NOT NULL DEFAULT '',
  `testcaseAddress` varchar(255) DEFAULT NULL,
  `env` varchar(64) DEFAULT NULL,
  `start_time` varchar(64) DEFAULT NULL,
  `execution_guid` varchar(64) DEFAULT NULL,
  `runtime` int(11),
  `state` varchar(64) DEFAULT NULL,
  `browser` varchar(64) DEFAULT NULL,
  `message` text,
  `stackTrace` text,
  `retryCount` int(11) DEFAULT '0',
  `exceptionMap_guid` varchar(64) DEFAULT NULL,
  `logURL` text,
  PRIMARY KEY (`guid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
