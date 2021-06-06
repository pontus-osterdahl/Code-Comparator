DROP TABLE IF EXISTS test_subject;

CREATE TABLE test_subject (
  id TEXT PRIMARY KEY,
  age_group TEXT NOT NULL,
  gender TEXT NOT NULL,
  occupation TEXT NOT NULL,
  other_occupation_description TEXT NOT NULL,
  occupation_time TEXT NOT NULL,
  software_development_frequency TEXT NOT NULL,
  programming_experience TEXT NOT NULL,

  java_course TEXT NOT NULL,
  rxjava_course TEXT NOT NULL,

  basic TEXT NOT NULL,
  prolog TEXT NOT NULL,
  haskell TEXT NOT NULL,
  java TEXT NOT NULL,
  sql TEXT NOT NULL,
  c TEXT NOT NULL,
  cpp TEXT NOT NULL,
  cs TEXT NOT NULL,
  python TEXT NOT NULL,
  javascript TEXT NOT NULL,
  assembly TEXT NOT NULL,

  java_knowledge TEXT NOT NULL,
  reactive_programming_experience TEXT NOT NULL,
  rxjava_knowledge TEXT NOT NULL,

  introduction_started TEXT NOT NULL,

  test_one TEXT,
  test_one_started TEXT,
  test_one_ended TEXT,
  test_one_duration_in_seconds TEXT,
  test_one_result TEXT,

  test_two TEXT,
  test_two_started TEXT,
  test_two_ended TEXT,
  test_two_duration_in_seconds TEXT,
  test_two_result TEXT,

  test_three TEXT,
  test_three_started TEXT,
  test_three_ended TEXT,
  test_three_duration_in_seconds TEXT,
  test_three_result TEXT,

  test_four TEXT,
  test_four_started TEXT,
  test_four_ended TEXT,
  test_four_duration_in_seconds TEXT,
  test_four_result TEXT
);