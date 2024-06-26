# hame.source_data

## Description

## Columns

| Name | Type | Default | Nullable | Children | Parents | Comment |
| ---- | ---- | ------- | -------- | -------- | ------- | ------- |
| type_of_source_data_id | uuid |  | false |  | [codes.type_of_source_data](codes.type_of_source_data.md) |  |
| name | jsonb | '{"eng": "", "fin": "", "swe": ""}'::jsonb | false |  |  |  |
| additional_information_uri | varchar |  | false |  |  |  |
| id | uuid | gen_random_uuid() | false |  |  |  |
| created_at | timestamp without time zone | now() | false |  |  |  |
| modified_at | timestamp without time zone | now() | false |  |  |  |
| detachment_date | timestamp without time zone |  | false |  |  |  |
| plan_id | uuid |  | false |  | [hame.plan](hame.plan.md) |  |

## Viewpoints

| Name | Definition |
| ---- | ---------- |
| [All tables](viewpoint-0.md) | All tables that make up maakuntakaava plan data. |

## Constraints

| Name | Type | Definition |
| ---- | ---- | ---------- |
| plan_id_fkey | FOREIGN KEY | FOREIGN KEY (plan_id) REFERENCES hame.plan(id) |
| type_of_source_data_id_fkey | FOREIGN KEY | FOREIGN KEY (type_of_source_data_id) REFERENCES codes.type_of_source_data(id) |
| source_data_pkey | PRIMARY KEY | PRIMARY KEY (id) |

## Indexes

| Name | Definition |
| ---- | ---------- |
| source_data_pkey | CREATE UNIQUE INDEX source_data_pkey ON hame.source_data USING btree (id) |

## Triggers

| Name | Definition |
| ---- | ---------- |
| trg_source_data_modified_at | CREATE TRIGGER trg_source_data_modified_at BEFORE INSERT OR UPDATE ON hame.source_data FOR EACH ROW EXECUTE FUNCTION hame.trgfunc_modified_at() |

## Relations

![er](hame.source_data.svg)

---

> Generated by [tbls](https://github.com/k1LoW/tbls)
