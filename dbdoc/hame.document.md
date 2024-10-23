# hame.document

## Description

## Columns

| Name | Type | Default | Nullable | Children | Parents | Comment |
| ---- | ---- | ------- | -------- | -------- | ------- | ------- |
| type_of_document_id | uuid |  | false |  | [codes.type_of_document](codes.type_of_document.md) |  |
| name | varchar |  | false |  |  |  |
| personal_details | varchar |  | false |  |  |  |
| publicity | varchar(11) |  | false |  |  |  |
| language | varchar |  | false |  |  |  |
| decision | boolean |  | false |  |  |  |
| decision_date | timestamp without time zone | now() | true |  |  |  |
| id | uuid | gen_random_uuid() | false |  |  |  |
| created_at | timestamp without time zone | now() | false |  |  |  |
| modified_at | timestamp without time zone | now() | false |  |  |  |
| plan_id | uuid |  | false |  | [hame.plan](hame.plan.md) |  |
| permanent_document_identifier | uuid |  | true |  |  |  |

## Viewpoints

| Name | Definition |
| ---- | ---------- |
| [All tables](viewpoint-0.md) | All tables that make up maakuntakaava plan data. |

## Constraints

| Name | Type | Definition |
| ---- | ---- | ---------- |
| plan_id_fkey | FOREIGN KEY | FOREIGN KEY (plan_id) REFERENCES hame.plan(id) |
| type_of_document_id_fkey | FOREIGN KEY | FOREIGN KEY (type_of_document_id) REFERENCES codes.type_of_document(id) |
| document_pkey | PRIMARY KEY | PRIMARY KEY (id) |

## Indexes

| Name | Definition |
| ---- | ---------- |
| document_pkey | CREATE UNIQUE INDEX document_pkey ON hame.document USING btree (id) |

## Triggers

| Name | Definition |
| ---- | ---------- |
| trg_document_modified_at | CREATE TRIGGER trg_document_modified_at BEFORE INSERT OR UPDATE ON hame.document FOR EACH ROW EXECUTE FUNCTION hame.trgfunc_modified_at() |

## Relations

![er](hame.document.svg)

---

> Generated by [tbls](https://github.com/k1LoW/tbls)