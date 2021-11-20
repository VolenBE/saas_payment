-- TABLE
CREATE TABLE Analytics
    (
        ID INT PRIMARY KEY NOT NULL,
        MRR INT NOT NULL,
        AAR INT NOT NULL,
        number_customers INT NOT NULL,
        average_revenue INT NOT NULL,
        company_id INT NOT NULL,
        FOREIGN KEY (company_id) REFERENCES Companies(company_id)
    );
CREATE TABLE Clients
    (
        client_id INT NOT NULL,
        invoice_ids_list VARCHAR,
        FOREIGN KEY (client_id) REFERENCES Users(id)
    );
CREATE TABLE Companies
    (
        company_id INT,
        vatid INT NOT NULL,
        client_ids_list VARCHAR,
        company_name VARCHAR NOT NULL,
        FOREIGN KEY (company_id) REFERENCES Users(ID)
    );
CREATE TABLE Invoices
    (
        invoice_id INT PRIMARY KEY NOT NULL,
        pending BOOLEAN,
        quote_id INT NOT NULL,
        FOREIGN KEY (quote_id) REFERENCES Quotes(quote_id)
    );
CREATE TABLE Prices
    (
        price_id INT PRIMARY KEY NOT NULL,
        amount INT NOT NULL,
        currency VARCHAR(64) NOT NULL,
        amount_euro INT NOT NULL
    );
CREATE TABLE Quotes
    (
        quote_id INT PRIMARY KEY NOT NULL,
        company_id INT NOT NULL,
        client_id INT NOT NULL,
        quantity INT NOT NULL,
        price_id INT NOT NULL,
        subscriptions_list VARCHAR,
        accepted BOOLEAN,
        FOREIGN KEY (company_id) REFERENCES Companies(company_id),
        FOREIGN KEY (client_id) REFERENCES Clients(client_id),
        FOREIGN KEY (price_id) REFERENCES Prices(price_id)
    );
CREATE TABLE Subscriptions
    (
        subscription_id INT PRIMARY KEY NOT NULL,
        name VARCHAR(64),
        active BOOLEAN,
        price_id INT NOT NULL,
        FOREIGN KEY(price_id) REFERENCES Prices(price_id)
    );
CREATE TABLE Users(
    ID INT PRIMARY KEY NOT NULL,
    username VARCHAR(64) NOT NULL,
    password VARCHAR(64) NOT NULL,
    bankaccount INT NOT NULL,
    address VARCHAR(128) NOT NULL);
 
-- INDEX
 
-- TRIGGER
 
-- VIEW
 
