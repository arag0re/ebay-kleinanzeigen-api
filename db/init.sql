-- Telegram chats
CREATE TABLE chat (
    id INTEGER PRIMARY KEY,          -- Telegram chat ID
    username TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Searches (one per user/request, containing many filters)
CREATE TABLE car_searches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT,
    model TEXT,
    car_type TEXT,
    shift_type TEXT,
    hu TEXT,                               -- Could be date/month string?
    fuel_type TEXT,
    power_from INTEGER,
    power_to INTEGER,
    ez_from TEXT,                          -- Erstzulassung (registration), possibly date or year
    ez_to TEXT,
    km_from INTEGER,
    km_to INTEGER,
    price_from INTEGER,
    price_to INTEGER,
    unlisted_car_model TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Found links per search
CREATE TABLE found_urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    search_id INTEGER NOT NULL,            -- Foreign key to search.id
    found_url TEXT NOT NULL,
    found_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (search_id) REFERENCES search(id)
);

CREATE INDEX idx_url_search_id ON found_urls(search_id);
