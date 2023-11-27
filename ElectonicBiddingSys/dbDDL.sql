-- Create the ElectronicBiddingSys database
CREATE DATABASE IF NOT EXISTS ElectronicBiddingSys;
USE ElectronicBiddingSys;

-- Create the User table
CREATE TABLE User (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Address VARCHAR(255),
    PhoneNumber VARCHAR(20),
    ProfilePicture BLOB, -- Binary Large Object for storing images
    PaymentDetails VARCHAR(255),
    UserType ENUM('Seller', 'Buyer') NOT NULL,
    -- constraint to check that the values allowed in the "UserType" column
    CONSTRAINT Check_UserType CHECK (UserType IN ('Seller', 'Buyer'))
);

-- Procedure to update user information
DELIMITER //
CREATE PROCEDURE UpdateUserInfo(
    IN p_UserID INT,
    IN p_Name VARCHAR(255),
    IN p_Address VARCHAR(255),
    IN p_PhoneNumber VARCHAR(20)
)
BEGIN
    UPDATE User
    SET Name = p_Name, Address = p_Address, PhoneNumber = p_PhoneNumber
    WHERE UserID = p_UserID;
END;
//
DELIMITER ;

    
-- Create a trigger to check password 
DELIMITER //
CREATE TRIGGER CheckPassword
BEFORE INSERT ON User
FOR EACH ROW
BEGIN
	-- The length of password has to be at least 8, contains at least one number and one letter
	IF LENGTH(NEW.Password) < 8 OR NOT (NEW.Password regexp '[0-9]') OR NOT (NEW.Password regexp '[a-zA-Z]') THEN
		SIGNAL SQLSTATE '45000'
		SET Message_Text = 'Password must be at least 8 characters and contain at least one number and one letter.';
    END IF;
END;
//
DELIMITER ;


-- Create a view to get the users' names and emails
CREATE VIEW UserNameandAddress AS
SELECT Name, Email
FROM User;


-- Create the Message table
CREATE TABLE Message (
    MessageID INT AUTO_INCREMENT PRIMARY KEY,
    ReceiverID INT,
    SenderID INT,
    Context TEXT,
    Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT FK_Receiver FOREIGN KEY (ReceiverID) REFERENCES User (UserID),
    CONSTRAINT FK_Sender FOREIGN KEY (SenderID) REFERENCES User (UserID)
);


-- Create the Item table
CREATE TABLE Item (
    ItemID INT AUTO_INCREMENT PRIMARY KEY,
    Description TEXT,
    Picture BLOB,
    Category VARCHAR(255),
    Cond VARCHAR(255), -- Condition
    Starting_price INT,
    End_date DATETIME,
    Start_date DATETIME
);


-- Create the Bid table
CREATE TABLE Bid(
	BidID INT AUTO_INCREMENT PRIMARY KEY,
    ItemID INT,
    UserID INT,
    Price INT,
    Status VARCHAR(255),
    CONSTRAINT FK_ItemID1 FOREIGN KEY (ItemID) REFERENCES Item (ItemID),
    CONSTRAINT FK_UserID1 FOREIGN KEY (UserID) REFERENCES User (UserID)
);
    

-- Create the Order table, I changed the 'Order' table to 'Orders' table
CREATE TABLE Orders(
	OrderID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    ItemID INT,
    OrderDate DATE,
    Status VARCHAR(255),
    TotalAmount INT,
    CONSTRAINT FK_UserID2 FOREIGN KEY (UserID) REFERENCES User (UserID),
    CONSTRAINT FK_ItemID2 FOREIGN KEY (ItemID) REFERENCES Item (ItemID)
);


-- Create the Admin table
CREATE TABLE Admin(
	AdminID INT AUTO_INCREMENT PRIMARY KEY,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Address VARCHAR(255),
    PhoneNumber VARCHAR(20),
    ProfilePicture BLOB
);

-- Create the delivery table
CREATE TABLE Delivery(
	DeliveryID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT,
    DeliveryStatus VARCHAR(255),
    EstimatedDeliveryDate DATE,
    CONSTRAINT FK_OrderID FOREIGN KEY (OrderID) REFERENCES Orders (OrderID)
);


-- Create the View History table
CREATE TABLE ViewHistory(
	UserID INT PRIMARY KEY,
    ItemID INT,
    Date DATE,
    CONSTRAINT FK_ItemID3 FOREIGN KEY (ItemID) REFERENCES Item (ItemID)
);
	
    
    
-- Create Transaction table
	CREATE TABLE Transaction(
		TransactionID INT AUTO_INCREMENT PRIMARY KEY,
        Type ENUM('Bank Transfer', 'Cash', 'Card'),
        TransactionDate DATE,
        TransactionStatus  ENUM('Completed', 'In Progress', 'Cancelled')
);


-- Create the Review table
CREATE TABLE Review(
	ReviewID INT AUTO_INCREMENT PRIMARY KEY,
    RevieweeID INT,
    ReviewerID INT,
    TransactionID INT,
    Rating INT CHECK (Rating BETWEEN 1 AND 5), -- Rating constraint
    Content TEXT,
    CONSTRAINT FK_RevieweeID FOREIGN KEY (RevieweeID) REFERENCES User (UserID),
    CONSTRAINT FK_ReviewerID FOREIGN KEY (ReviewerID) REFERENCES User (UserID),
    CONSTRAINT FK_TransactionID FOREIGN KEY (TransactionID) REFERENCES Transaction (TransactionID)
);


        











