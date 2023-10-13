--  creating a trigge that decreases an item quantity
-- after an order of the item is made ...

CREATE TRIGGER decrease_item 
AFTER INSERT ON orders FOR EACH ROW
UPDATE items
SET quantity = quantity - NEW.number
WHERE name = NEW.item_name;
