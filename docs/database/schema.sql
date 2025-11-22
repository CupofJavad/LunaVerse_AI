-- Lunaverse Show Brain Database Schema

-- Users table
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('admin','pm','viewer')),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Events table
CREATE TABLE IF NOT EXISTS events (
  id UUID PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),

  event_name TEXT NOT NULL,
  client_name TEXT,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,

  venue TEXT NOT NULL,
  city TEXT NOT NULL,
  state TEXT NOT NULL,
  country TEXT NOT NULL,
  timezone TEXT NOT NULL,
  expected_attendance INTEGER,

  current_opportunity_id TEXT,
  current_organization_id TEXT,
  current_contact_id TEXT,
  current_venue_id TEXT,
  opportunity_status TEXT,

  custom_fields JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Rooms table
CREATE TABLE IF NOT EXISTS rooms (
  id UUID PRIMARY KEY,
  event_id UUID REFERENCES events(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  type TEXT,
  capacity INTEGER,
  days_active JSONB,
  layout TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Room requirements table
CREATE TABLE IF NOT EXISTS room_requirements (
  id UUID PRIMARY KEY,
  room_id UUID REFERENCES rooms(id) ON DELETE CASCADE,
  audio JSONB,
  video JSONB,
  lighting JSONB,
  staging JSONB,
  power JSONB,
  schedule JSONB,
  other_notes TEXT
);

-- Current products table
CREATE TABLE IF NOT EXISTS current_products (
  id UUID PRIMARY KEY,
  current_product_id TEXT,
  name TEXT,
  description TEXT,
  product_group_name TEXT,
  product_group_desc TEXT,
  is_bulk_stock BOOLEAN,
  is_serialised_stock BOOLEAN,
  is_non_stock BOOLEAN,
  rental_price NUMERIC,
  rental_charge_period_name TEXT,
  rental_rate_definition_name TEXT,
  rental_revenue_group TEXT,
  sale_price NUMERIC,
  sale_revenue_group TEXT,
  replacement_charge NUMERIC,
  weight NUMERIC,
  power NUMERIC,
  barcode TEXT,
  icon_url TEXT,
  raw_json JSONB,
  embedding JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_current_products_product_id ON current_products(current_product_id);
CREATE INDEX IF NOT EXISTS idx_current_products_group ON current_products(product_group_name);

-- Current stock levels table
CREATE TABLE IF NOT EXISTS current_stock_levels (
  id UUID PRIMARY KEY,
  current_product_id UUID REFERENCES current_products(id) ON DELETE CASCADE,
  current_stock_level_id TEXT,
  is_serialised BOOLEAN,
  asset_number TEXT,
  store_name TEXT,
  quantity INTEGER,
  status TEXT,
  custom_fields JSONB,
  raw_json JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Event plans table
CREATE TABLE IF NOT EXISTS event_plans (
  id UUID PRIMARY KEY,
  event_id UUID REFERENCES events(id) ON DELETE CASCADE,
  summary TEXT,
  assumptions JSONB,
  trucking JSONB,
  metadata JSONB,
  weight_total_lbs NUMERIC,
  weight_by_room JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Equipment lines table
CREATE TABLE IF NOT EXISTS equipment_lines (
  id UUID PRIMARY KEY,
  event_plan_id UUID REFERENCES event_plans(id) ON DELETE CASCADE,
  room_id UUID REFERENCES rooms(id) ON DELETE CASCADE,

  opportunity_group_name TEXT,
  opportunity_group_order INTEGER,

  current_product_id UUID REFERENCES current_products(id),
  current_stock_level_id UUID REFERENCES current_stock_levels(id),

  item_code TEXT,
  name TEXT,
  product_group_name TEXT,
  category TEXT,
  qty NUMERIC,
  unit_type TEXT,
  rental_price NUMERIC,
  replacement_charge NUMERIC,
  weight_total NUMERIC,

  is_accessory BOOLEAN,
  parent_equipment_line_id UUID,

  notes TEXT,
  source TEXT
);

-- Crew lines table
CREATE TABLE IF NOT EXISTS crew_lines (
  id UUID PRIMARY KEY,
  event_plan_id UUID REFERENCES event_plans(id) ON DELETE CASCADE,
  room_id UUID REFERENCES rooms(id) ON DELETE CASCADE,
  role TEXT,
  qty INTEGER,
  hours_in NUMERIC,
  hours_show NUMERIC,
  hours_out NUMERIC,
  bill_rate NUMERIC,
  total_bill NUMERIC,
  notes TEXT
);

-- Historic events table
CREATE TABLE IF NOT EXISTS historic_events (
  id UUID PRIMARY KEY,
  title TEXT,
  body TEXT,
  embedding JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Template documents table
CREATE TABLE IF NOT EXISTS template_documents (
  id UUID PRIMARY KEY,
  title TEXT,
  body TEXT,
  doc_type TEXT,
  embedding JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

