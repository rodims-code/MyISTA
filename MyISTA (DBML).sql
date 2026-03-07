CREATE TABLE "users" (
  "id" integer PRIMARY KEY,
  "matricule" varchar UNIQUE NOT NULL,
  "username" varchar NOT NULL,
  "niveau" varchar NOT NULL,
  "filiere" varchar NOT NULL,
  "role" varchar NOT NULL DEFAULT 'student',
  "date_inscription" timestamp DEFAULT (now())
);

CREATE TABLE "batiments" (
  "id" integer PRIMARY KEY,
  "nom" varchar NOT NULL,
  "description" varchar
);

CREATE TABLE "salles" (
  "id" integer PRIMARY KEY,
  "nom" varchar NOT NULL,
  "batiment_id" integer NOT NULL
);

CREATE TABLE "affectation_salles" (
  "id" integer PRIMARY KEY,
  "niveau" varchar NOT NULL,
  "filiere" varchar NOT NULL,
  "salle_id" integer NOT NULL
);

CREATE TABLE "infos_essentielles" (
  "id" integer PRIMARY KEY,
  "titre" varchar NOT NULL,
  "contenu" text NOT NULL,
  "categorie" varchar,
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "documents" (
  "id" integer PRIMARY KEY,
  "titre" varchar NOT NULL,
  "fichier_url" varchar NOT NULL,
  "niveau" varchar NOT NULL,
  "filiere" varchar NOT NULL,
  "cours" varchar NOT NULL,
  "uploader_id" integer NOT NULL,
  "date_upload" timestamp DEFAULT (now())
);

ALTER TABLE "salles" ADD FOREIGN KEY ("batiment_id") REFERENCES "batiments" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "affectation_salles" ADD FOREIGN KEY ("salle_id") REFERENCES "salles" ("id") DEFERRABLE INITIALLY IMMEDIATE;

ALTER TABLE "documents" ADD FOREIGN KEY ("uploader_id") REFERENCES "users" ("id") DEFERRABLE INITIALLY IMMEDIATE;
