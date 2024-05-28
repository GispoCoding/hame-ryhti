# codes.type_of_document

## Description

## Columns

| Name | Type | Default | Nullable | Children | Parents | Comment |
| ---- | ---- | ------- | -------- | -------- | ------- | ------- |
| value | varchar |  | false |  |  |  |
| short_name | varchar | ''::character varying | false |  |  |  |
| name | jsonb | '{"eng": "", "fin": "", "swe": ""}'::jsonb | false |  |  |  |
| description | jsonb | '{"eng": "", "fin": "", "swe": ""}'::jsonb | false |  |  |  |
| status | varchar |  | false |  |  |  |
| level | integer | 1 | false |  |  |  |
| parent_id | uuid |  | true |  | [codes.type_of_document](codes.type_of_document.md) |  |
| id | uuid | gen_random_uuid() | false | [codes.type_of_document](codes.type_of_document.md) [hame.document](hame.document.md) |  |  |
| created_at | timestamp without time zone | now() | false |  |  |  |
| modified_at | timestamp without time zone | now() | false |  |  |  |

## Viewpoints

| Name | Definition |
| ---- | ---------- |
| [All tables](viewpoint-0.md) | All tables that make up maakuntakaava plan data. |

## Constraints

| Name | Type | Definition |
| ---- | ---- | ---------- |
| type_of_document_parent_id_fkey | FOREIGN KEY | FOREIGN KEY (parent_id) REFERENCES codes.type_of_document(id) |
| type_of_document_pkey | PRIMARY KEY | PRIMARY KEY (id) |

## Indexes

| Name | Definition |
| ---- | ---------- |
| type_of_document_pkey | CREATE UNIQUE INDEX type_of_document_pkey ON codes.type_of_document USING btree (id) |
| ix_codes_type_of_document_level | CREATE INDEX ix_codes_type_of_document_level ON codes.type_of_document USING btree (level) |
| ix_codes_type_of_document_parent_id | CREATE INDEX ix_codes_type_of_document_parent_id ON codes.type_of_document USING btree (parent_id) |
| ix_codes_type_of_document_value | CREATE UNIQUE INDEX ix_codes_type_of_document_value ON codes.type_of_document USING btree (value) |
| ix_codes_type_of_document_short_name | CREATE INDEX ix_codes_type_of_document_short_name ON codes.type_of_document USING btree (short_name) |

## Relations

![er](codes.type_of_document.svg)

---

> Generated by [tbls](https://github.com/k1LoW/tbls)