# hame.plan_proposition

## Description

## Columns

| Name | Type | Default | Nullable | Children | Parents | Comment |
| ---- | ---- | ------- | -------- | -------- | ------- | ------- |
| plan_regulation_group_id | uuid |  | false |  | [hame.plan_regulation_group](hame.plan_regulation_group.md) |  |
| text_value | jsonb | '{"eng": "", "fin": "", "swe": ""}'::jsonb | false |  |  |  |
| ordering | integer |  | true |  |  |  |
| exported_at | timestamp without time zone |  | true |  |  |  |
| lifecycle_status_id | uuid |  | false |  | [codes.lifecycle_status](codes.lifecycle_status.md) |  |
| id | uuid | gen_random_uuid() | false | [hame.lifecycle_date](hame.lifecycle_date.md) |  |  |
| created_at | timestamp without time zone | now() | false |  |  |  |
| modified_at | timestamp without time zone | now() | false |  |  |  |
| name | jsonb | '{"eng": "", "fin": "", "swe": ""}'::jsonb | false |  |  |  |
| plan_theme_id | uuid |  | true |  | [codes.plan_theme](codes.plan_theme.md) |  |

## Viewpoints

| Name | Definition |
| ---- | ---------- |
| [All tables](viewpoint-0.md) | All tables that make up maakuntakaava plan data. |

## Constraints

| Name | Type | Definition |
| ---- | ---- | ---------- |
| plan_lifecycle_status_id_fkey | FOREIGN KEY | FOREIGN KEY (lifecycle_status_id) REFERENCES codes.lifecycle_status(id) |
| plan_regulation_group_id_fkey | FOREIGN KEY | FOREIGN KEY (plan_regulation_group_id) REFERENCES hame.plan_regulation_group(id) |
| plan_proposition_pkey | PRIMARY KEY | PRIMARY KEY (id) |
| plan_theme_id_fkey | FOREIGN KEY | FOREIGN KEY (plan_theme_id) REFERENCES codes.plan_theme(id) |

## Indexes

| Name | Definition |
| ---- | ---------- |
| plan_proposition_pkey | CREATE UNIQUE INDEX plan_proposition_pkey ON hame.plan_proposition USING btree (id) |
| ix_hame_plan_proposition_ordering | CREATE INDEX ix_hame_plan_proposition_ordering ON hame.plan_proposition USING btree (ordering) |
| ix_hame_plan_proposition_lifecycle_status_id | CREATE INDEX ix_hame_plan_proposition_lifecycle_status_id ON hame.plan_proposition USING btree (lifecycle_status_id) |

## Triggers

| Name | Definition |
| ---- | ---------- |
| trg_plan_proposition_modified_at | CREATE TRIGGER trg_plan_proposition_modified_at BEFORE INSERT OR UPDATE ON hame.plan_proposition FOR EACH ROW EXECUTE FUNCTION hame.trgfunc_modified_at() |
| trg_plan_proposition_new_lifecycle_date | CREATE TRIGGER trg_plan_proposition_new_lifecycle_date BEFORE UPDATE ON hame.plan_proposition FOR EACH ROW WHEN ((new.lifecycle_status_id <> old.lifecycle_status_id)) EXECUTE FUNCTION hame.trgfunc_plan_proposition_new_lifecycle_date() |

## Relations

![er](hame.plan_proposition.svg)

---

> Generated by [tbls](https://github.com/k1LoW/tbls)
