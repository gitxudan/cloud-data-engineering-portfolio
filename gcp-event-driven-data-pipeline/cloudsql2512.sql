USE petstore;
SELECT * FROM customer;

truncate table customer;

LOAD DATA
	local infile 'C:/Users/Think/Desktop/Python/2512/data/customer.txt'
    INTO TABLE customer
    LINES terminated by '\r\n'
    IGNORE 1 lines
;
    
SET SESSION local_infile = 1    
