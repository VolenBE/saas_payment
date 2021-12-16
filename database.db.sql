BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Users" (
	"ID"	INTEGER NOT NULL,
	"username"	VARCHAR(64) NOT NULL,
	"password"	VARCHAR(64) NOT NULL,
	"bankaccount"	INT NOT NULL,
	"address"	VARCHAR(128) NOT NULL,
	PRIMARY KEY("ID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Companies" (
	"company_id"	INT,
	"vatid"	INT NOT NULL,
	"company_name"	VARCHAR NOT NULL,
	FOREIGN KEY("company_id") REFERENCES "Users"("ID")
);
CREATE TABLE IF NOT EXISTS "Clients" (
	"client_id"	INT NOT NULL,
	"company_id"	INT NOT NULL,
	FOREIGN KEY("company_id") REFERENCES "Companies"("company_id"),
	FOREIGN KEY("client_id") REFERENCES "Users"("id")
);
CREATE TABLE IF NOT EXISTS "Analytics" (
	"ID"	INTEGER NOT NULL,
	"MRR"	INT NOT NULL,
	"AAR"	INT NOT NULL,
	"number_customers"	INT NOT NULL,
	"average_revenue"	INT NOT NULL,
	"company_id"	INT NOT NULL,
	PRIMARY KEY("ID" AUTOINCREMENT),
	FOREIGN KEY("company_id") REFERENCES "Companies"("company_id")
);
CREATE TABLE IF NOT EXISTS "Quotes" (
	"quote_id"	INTEGER NOT NULL,
	"company_id"	INT NOT NULL,
	"client_id"	INT NOT NULL,
	"quantity"	INT NOT NULL,
	"subscriptions_list"	VARCHAR(248),
	"price_eur"	INT NOT NULL,
	"accepted"	BOOLEAN,
	PRIMARY KEY("quote_id" AUTOINCREMENT),
	FOREIGN KEY("client_id") REFERENCES "Clients"("client_id"),
	FOREIGN KEY("company_id") REFERENCES "Companies"("company_id")
);
CREATE TABLE IF NOT EXISTS "Invoices" (
	"invoice_id"	INTEGER NOT NULL,
	"pending"	BOOLEAN,
	"client_id"	INT NOT NULL,
	"quote_id"	INT NOT NULL,
	"amount"	INT NOT NULL,
	PRIMARY KEY("invoice_id" AUTOINCREMENT),
	FOREIGN KEY("client_id") REFERENCES "clients"("client_id"),
	FOREIGN KEY("quote_id") REFERENCES "Quotes"("quote_id")
);
CREATE TABLE IF NOT EXISTS "Payments" (
	"payment_id"	INTEGER NOT NULL,
	"invoice_id"	INT NOT NULL,
	"amount_eur"	INT NOT NULL,
	"currency_name"	char(3) NOT NULL,
	"amount_currency"	INT NOT NULL,
	"success"	BOOLEAN NOT NULL,
	"LastPaymentDate"	TIMESTAMP,
	PRIMARY KEY("payment_id" AUTOINCREMENT),
	FOREIGN KEY("invoice_id") REFERENCES "Invoices"("invoice_id")
);
CREATE TABLE IF NOT EXISTS "Subscriptions" (
	"subscription_id"	INTEGER NOT NULL,
	"name"	VARCHAR(64),
	"client_id"	INT NOT NULL,
	"status"	INT NOT NULL,
	"price"	INT NOT NULL,
	PRIMARY KEY("subscription_id" AUTOINCREMENT),
	FOREIGN KEY("client_id") REFERENCES "Clients"("client_id")
);
CREATE TABLE IF NOT EXISTS "Currencies" (
	"currency_id"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"rate"	INT NOT NULL,
	PRIMARY KEY("currency_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Tech" (
	"LastReset"	TIMESTAMP
);
INSERT INTO "Users" VALUES (1,'vitiated','FDm641A5',80576219,'92 rue de la Thyria, Charleroi');
INSERT INTO "Users" VALUES (2,'argentinaargentine','2AD1mBzi',98253071,'20 rue Roosevelt, Namur');
INSERT INTO "Users" VALUES (3,'fontainebleau','z2D36FeA',71452809,'91 rue Roosevelt, Bruxelles');
INSERT INTO "Users" VALUES (4,'macmacabre','73Fz6A2i',36925874,'48 rue des Monthys, Bruxelles');
INSERT INTO "Users" VALUES (5,'kenyakenyatta','D9z5e2B3',47953016,'21 rue des Marroniers, Liège');
INSERT INTO "Users" VALUES (6,'quench','8D3ei7FB',15204986,'24 rue de la Thyria, Charleroi');
INSERT INTO "Users" VALUES (7,'jamal','mDB32e61',4937825,'56 rue Roosevelt, Bruxelles');
INSERT INTO "Users" VALUES (8,'nations','B6DF94m2',29370864,'26 rue des Marroniers, Namur');
INSERT INTO "Users" VALUES (9,'expectorate','5eFiB163',41967385,'22 rue des Marroniers, Liège');
INSERT INTO "Users" VALUES (10,'copeland','7BF941z2',8139654,'57 rue des Marroniers, Bruxelles');
INSERT INTO "Users" VALUES (11,'electrum','B4A3m827',92104637,'23 rue de la Thyria, Charleroi');
INSERT INTO "Users" VALUES (12,'unleash','2175A4i6',58072691,'65 rue des Marroniers, Liège');
INSERT INTO "Users" VALUES (13,'advancement','F378z526',97831450,'76 rue Roosevelt, Charleroi');
INSERT INTO "Users" VALUES (14,'canterbury','m76ezF18',28509436,'35 rue Neuve, Liège');
INSERT INTO "Users" VALUES (15,'ginsberg','zA29i4D3',78629514,'58 rue des Monthys, Charleroi');
INSERT INTO "Users" VALUES (16,'sky','49eBF2i5',15287643,'63 rue Roosevelt, Liège');
INSERT INTO "Users" VALUES (17,'ameba','e5FADi23',60824391,'2 rue des Monthys, Liège');
INSERT INTO "Users" VALUES (18,'conserve','F4m8932B',32096581,'41 rue de la Thyria, Liège');
INSERT INTO "Users" VALUES (19,'christensen','3z56D1ei',9453216,'95 rue des Marroniers, Bruxelles');
INSERT INTO "Users" VALUES (20,'cashew','9B8FzeA5',37826105,'9 rue Neuve, Bruxelles');
INSERT INTO "Users" VALUES (21,'laux','1B7FDezA',13647902,'75 rue Neuve, Charleroi');
INSERT INTO "Users" VALUES (22,'duumvirate','43mFe92z',65092738,'70 rue de la Thyria, Bruxelles');
INSERT INTO "Users" VALUES (23,'omphale','3z9F158m',61487259,'89 rue des Marroniers, Namur');
INSERT INTO "Users" VALUES (24,'eldwon','6F7im8D2',70316849,'44 rue des Marroniers, Charleroi');
INSERT INTO "Users" VALUES (25,'marauding','4iBze9m1',45703962,'33 rue Neuve, Charleroi');
INSERT INTO "Users" VALUES (26,'pavlodar','753e92z6',8796154,'70 rue des Marroniers, Charleroi');
INSERT INTO "Users" VALUES (27,'edieedification','12z6A53e',47986035,'62 rue de la Thyria, Charleroi');
INSERT INTO "Users" VALUES (28,'impel','7e9z5iF2',48519362,'38 rue Roosevelt, Liège');
INSERT INTO "Users" VALUES (29,'peptidase','FmAi59B6',95104768,'52 rue Neuve, Bruxelles');
INSERT INTO "Users" VALUES (30,'stomodaeum','7ezF659m',52174869,'97 rue des Monthys, Charleroi');
INSERT INTO "Users" VALUES (31,'crafty','z37ieB29',94583612,'70 rue de la Thyria, Liège');
INSERT INTO "Users" VALUES (32,'pentalpha','eBA9D5z7',48075932,'35 rue des Monthys, Bruxelles');
INSERT INTO "Users" VALUES (33,'evanesce','3ze9mDi8',71869024,'55 rue des Monthys, Bruxelles');
INSERT INTO "Users" VALUES (34,'gorman','iBz2meA5',63758940,'48 rue Neuve, Namur');
INSERT INTO "Users" VALUES (35,'handmedown','Di718F6e',83541076,'90 rue Neuve, Liège');
INSERT INTO "Users" VALUES (36,'bosom','47A28e5B',68329704,'22 rue Roosevelt, Charleroi');
INSERT INTO "Users" VALUES (37,'bedim','85mziF27',97136248,'36 rue Roosevelt, Namur');
INSERT INTO "Users" VALUES (38,'invar','BDmF76zi',98036542,'95 rue Neuve, Namur');
INSERT INTO "Users" VALUES (39,'philology','823meFi7',30592471,'96 rue Neuve, Namur');
INSERT INTO "Users" VALUES (40,'arriviste','BmAz462i',10329485,'45 rue de la Thyria, Namur');
INSERT INTO "Users" VALUES (41,'outbalance','51mz934e',29817643,'87 rue des Marroniers, Namur');
INSERT INTO "Users" VALUES (42,'macmullin','4mA27519',9271483,'70 rue de la Thyria, Namur');
INSERT INTO "Users" VALUES (43,'empyreal','8m6z15AD',74238069,'74 rue Neuve, Liège');
INSERT INTO "Users" VALUES (44,'defibrillator','3A84i5F2',76913280,'1 rue Roosevelt, Liège');
INSERT INTO "Users" VALUES (45,'scopula','A715BFzD',80651243,'53 rue des Marroniers, Namur');
INSERT INTO "Users" VALUES (46,'basham','3BzemA51',74398501,'82 rue Neuve, Charleroi');
INSERT INTO "Users" VALUES (47,'mannerheim','F9e371zA',10472368,'27 rue des Marroniers, Liège');
INSERT INTO "Users" VALUES (48,'fairspoken','4A56127F',63840271,'22 rue des Monthys, Charleroi');
INSERT INTO "Users" VALUES (49,'upstart','iDBz2me5',81753946,'48 rue Neuve, Bruxelles');
INSERT INTO "Users" VALUES (50,'headway','D15zA86i',96542783,'4 rue de la Thyria, Charleroi');
INSERT INTO "Users" VALUES (51,'baskerville','me8Biz4A',46035928,'81 rue de la Thyria, Bruxelles');
INSERT INTO "Users" VALUES (52,'amphictyony','Fz258m64',10428695,'5 rue Roosevelt, Bruxelles');
INSERT INTO "Users" VALUES (53,'merylmes','z5i397AF',24053896,'54 rue de la Thyria, Liège');
INSERT INTO "Users" VALUES (54,'generalization','7AeD95zF',35140698,'29 rue Roosevelt, Charleroi');
INSERT INTO "Users" VALUES (55,'decoupage','iAm2B4F1',26897510,'73 rue des Marroniers, Liège');
INSERT INTO "Users" VALUES (56,'screech','FDe93ABz',82415793,'58 rue Neuve, Bruxelles');
INSERT INTO "Companies" VALUES (1,27180496,'Capitalcorp');
INSERT INTO "Companies" VALUES (2,6549371,'Atlas Architectural Designs');
INSERT INTO "Companies" VALUES (3,28167034,'Chargepal');
INSERT INTO "Companies" VALUES (4,20863571,'Alert Alarm Company');
INSERT INTO "Companies" VALUES (5,3297861,'Dream Home Real Estate Service');
INSERT INTO "Companies" VALUES (6,32907461,'Gamma Grays');
INSERT INTO "Companies" VALUES (7,85470296,'Afforda Merchant Services');
INSERT INTO "Companies" VALUES (8,43019568,'Future Bright');
INSERT INTO "Companies" VALUES (9,28347065,'First Choice Garden Maintenance');
INSERT INTO "Companies" VALUES (10,37021845,'Earthworks Garden Kare');
INSERT INTO "Companies" VALUES (11,91406528,'Corinthian Designs');
INSERT INTO "Companies" VALUES (12,85490376,'Architectural Genie');
INSERT INTO "Companies" VALUES (13,60875132,'Flexus');
INSERT INTO "Companies" VALUES (14,70316894,'Bountiful Harvest Health Food Store');
INSERT INTO "Companies" VALUES (29,76805314,'Lawnscape Garden Maintenance');
INSERT INTO "Companies" VALUES (30,3428561,'Fragrant Flower Lawn Services');
INSERT INTO "Companies" VALUES (31,38596014,'Beasts of Beauty');
INSERT INTO "Companies" VALUES (32,20198543,'Formula Gray');
INSERT INTO "Companies" VALUES (33,70431589,'Castle Realty');
INSERT INTO "Companies" VALUES (34,30892465,'Intelacard');
INSERT INTO "Companies" VALUES (35,7569413,'Creative Wealth');
INSERT INTO "Companies" VALUES (36,69021834,'Integra Wealth Planners');
INSERT INTO "Companies" VALUES (37,92831650,'Life Map');
INSERT INTO "Companies" VALUES (38,17945063,'EnviroSource Design');
INSERT INTO "Companies" VALUES (39,39658702,'Fellowship Investments');
INSERT INTO "Companies" VALUES (40,14730895,'First Rate Choice');
INSERT INTO "Companies" VALUES (41,2486531,'Four Leaf Clover');
INSERT INTO "Companies" VALUES (42,19463208,'Castle Realty');
INSERT INTO "Clients" VALUES (15,4);
INSERT INTO "Clients" VALUES (16,11);
INSERT INTO "Clients" VALUES (17,3);
INSERT INTO "Clients" VALUES (18,13);
INSERT INTO "Clients" VALUES (19,1);
INSERT INTO "Clients" VALUES (20,13);
INSERT INTO "Clients" VALUES (21,5);
INSERT INTO "Clients" VALUES (22,2);
INSERT INTO "Clients" VALUES (23,4);
INSERT INTO "Clients" VALUES (24,11);
INSERT INTO "Clients" VALUES (25,12);
INSERT INTO "Clients" VALUES (26,7);
INSERT INTO "Clients" VALUES (27,12);
INSERT INTO "Clients" VALUES (28,14);
INSERT INTO "Clients" VALUES (43,29);
INSERT INTO "Clients" VALUES (44,6);
INSERT INTO "Clients" VALUES (45,29);
INSERT INTO "Clients" VALUES (46,6);
INSERT INTO "Clients" VALUES (47,13);
INSERT INTO "Clients" VALUES (48,10);
INSERT INTO "Clients" VALUES (49,35);
INSERT INTO "Clients" VALUES (50,6);
INSERT INTO "Clients" VALUES (51,34);
INSERT INTO "Clients" VALUES (52,3);
INSERT INTO "Clients" VALUES (53,2);
INSERT INTO "Clients" VALUES (54,7);
INSERT INTO "Clients" VALUES (55,14);
INSERT INTO "Clients" VALUES (56,33);
INSERT INTO "Subscriptions" VALUES (1,'First Rate Choice',17,0,28);
INSERT INTO "Subscriptions" VALUES (2,'Formula Gray',51,0,94);
INSERT INTO "Subscriptions" VALUES (3,'Creative Wealth',19,0,22);
INSERT INTO "Subscriptions" VALUES (4,'Life Map',15,0,82);
INSERT INTO "Subscriptions" VALUES (5,'Alert Alarm Company',45,0,71);
INSERT INTO "Subscriptions" VALUES (6,'Corinthian Designs',21,0,76);
INSERT INTO "Subscriptions" VALUES (7,'Future Bright',48,0,24);
INSERT INTO "Subscriptions" VALUES (8,'Architectural Genie',17,0,64);
INSERT INTO "Subscriptions" VALUES (9,'Creative Wealth',54,0,50);
INSERT INTO "Subscriptions" VALUES (10,'Castle Realty',45,0,41);
INSERT INTO "Subscriptions" VALUES (11,'Formula Gray',20,0,73);
INSERT INTO "Subscriptions" VALUES (12,'Four Leaf Clover',44,0,94);
INSERT INTO "Subscriptions" VALUES (13,'Architectural Genie',53,0,47);
INSERT INTO "Subscriptions" VALUES (14,'Castle Realty',48,0,72);
COMMIT;
