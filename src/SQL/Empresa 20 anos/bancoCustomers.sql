CREATE TABLE Customers {
  id NUMERIC PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  street VARCHAR(80) NOT NULL,
  city VARCHAR(80) NOT NULL,
  state CHAR (2),
  credit_limit NUMERIC(10,2)
};