/*
 * Copyright 2020, Google LLC.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */


INSERT INTO users VALUES
('1011226111', 'testuser', '\x243262243132244c48334f54422e70653274596d6834534b756673727563564b3848774630494d2f34717044746868366e42352e744b575978314e61', 'Test', 'User', '2000-01-01', '-5', 'Bowling Green, New York City', 'NY', '10004', '111-22-3333'),
('1033623433', 'alice', '\x243262243132244c48334f54422e70653274596d6834534b756673727563564b3848774630494d2f34717044746868366e42352e744b575978314e61', 'Alice', 'User', '2000-01-01', '-5', 'Bowling Green, New York City', 'NY', '10004', '111-22-3333'),
('1055757655', 'bob', '\x243262243132244c48334f54422e70653274596d6834534b756673727563564b3848774630494d2f34717044746868366e42352e744b575978314e61', 'Bob', 'User', '2000-01-01', '-5', 'Bowling Green, New York City', 'NY', '10004', '111-22-3333'),
('1077441377', 'eve', '\x243262243132244c48334f54422e70653274596d6834534b756673727563564b3848774630494d2f34717044746868366e42352e744b575978314e61', 'Eve', 'User', '2000-01-01', '-5', 'Bowling Green, New York City', 'NY', '10004', '111-22-3333')
ON CONFLICT DO NOTHING;

INSERT INTO contacts VALUES
('testuser', 'Alice', '1033623433', '883745000', 'false'),
('testuser', 'Bob', '1055757655', '883745000', 'false'),
('testuser', 'Eve', '1077441377', '883745000', 'false'),
('alice', 'Testuser', '1011226111', '883745000', 'false'),
('alice', 'Bob', '1055757655', '883745000', 'false'),
('alice', 'Eve', '1077441377', '883745000', 'false'),
('bob', 'Testuser', '1011226111', '883745000', 'false'),
('bob', 'Alice', '1033623433', '883745000', 'false'),
('bob', 'Eve', '1077441377', '883745000', 'false'),
('eve', 'Testuser', '1011226111', '883745000', 'false'),
('eve', 'Alice', '1033623433', '883745000', 'false'),
('eve', 'Bob', '1055757655', '883745000', 'false')
ON CONFLICT DO NOTHING;

INSERT INTO contacts VALUES
('testuser', 'External Bank', '9099791699', '808889588', 'true'),
('alice', 'External Bank', '9099791699', '808889588', 'true'),
('bob', 'External Bank', '9099791699', '808889588', 'true'),
('eve', 'External Bank', '9099791699', '808889588', 'true')
ON CONFLICT DO NOTHING;

-- Add merchant contacts for testuser (for AI analysis)
INSERT INTO contacts VALUES
('testuser', 'Starbucks Coffee', '2001001001', '883745000', 'true'),
('testuser', 'Whole Foods Market', '2001001002', '883745000', 'true'),
('testuser', 'Amazon.com', '2001001003', '883745000', 'true'),
('testuser', 'Shell Gas Station', '2001001004', '883745000', 'true'),
('testuser', 'McDonald''s', '2001001005', '883745000', 'true'),
('testuser', 'Target', '2001001006', '883745000', 'true'),
('testuser', 'Uber', '2001001007', '883745000', 'true'),
('testuser', 'Netflix', '2001001008', '883745000', 'true'),
('testuser', 'Best Buy', '2001001009', '883745000', 'true'),
('testuser', 'Chipotle Mexican Grill', '2001001010', '883745000', 'true'),
('testuser', 'CVS Pharmacy', '2001001011', '883745000', 'true'),
('testuser', 'Spotify', '2001001012', '883745000', 'true'),
('testuser', 'Apple Store', '2001001013', '883745000', 'true'),
('testuser', 'Costco Wholesale', '2001001014', '883745000', 'true'),
('testuser', 'Planet Fitness', '2001001015', '883745000', 'true'),
('testuser', 'Panera Bread', '2001001016', '883745000', 'true'),
('testuser', 'Home Depot', '2001001017', '883745000', 'true'),
('testuser', 'Safeway', '2001001018', '883745000', 'true'),
('testuser', 'Lyft', '2001001019', '883745000', 'true'),
('testuser', 'Adobe Creative Cloud', '2001001020', '883745000', 'true')
ON CONFLICT DO NOTHING;
