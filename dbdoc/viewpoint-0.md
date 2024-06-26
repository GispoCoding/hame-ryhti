# All tables

## Description

All tables that make up maakuntakaava plan data.

## Tables

### Plan geometry tables

These tables represent all geometries in the plan.

| Name | Columns | Comment | Type |
| ---- | ------- | ------- | ---- |
| [hame.plan](hame.plan.md) | 18 |  | BASE TABLE |
| [hame.land_use_area](hame.land_use_area.md) | 15 |  | BASE TABLE |
| [hame.land_use_point](hame.land_use_point.md) | 15 |  | BASE TABLE |
| [hame.line](hame.line.md) | 15 |  | BASE TABLE |
| [hame.other_area](hame.other_area.md) | 15 |  | BASE TABLE |
| [hame.other_point](hame.other_point.md) | 15 |  | BASE TABLE |

### Plan regulation tables

These tables represent all regulations in the plan.

| Name | Columns | Comment | Type |
| ---- | ------- | ------- | ---- |
| [hame.plan_regulation_group](hame.plan_regulation_group.md) | 6 |  | BASE TABLE |
| [hame.plan_regulation](hame.plan_regulation.md) | 23 |  | BASE TABLE |
| [hame.plan_proposition](hame.plan_proposition.md) | 10 |  | BASE TABLE |

### Plan metadata tables

These tables contain all metadata, documents and other linked information.

| Name | Columns | Comment | Type |
| ---- | ------- | ------- | ---- |
| [hame.source_data](hame.source_data.md) | 8 |  | BASE TABLE |
| [hame.organisation](hame.organisation.md) | 6 |  | BASE TABLE |
| [hame.document](hame.document.md) | 12 |  | BASE TABLE |
| [hame.lifecycle_date](hame.lifecycle_date.md) | 14 |  | BASE TABLE |

### Code tables

These tables contain all national (koodistot.suomi.fi) and local codes used for classifying plan data.

| Name | Columns | Comment | Type |
| ---- | ------- | ------- | ---- |
| [codes.lifecycle_status](codes.lifecycle_status.md) | 10 |  | BASE TABLE |
| [codes.plan_type](codes.plan_type.md) | 10 |  | BASE TABLE |
| [codes.type_of_additional_information](codes.type_of_additional_information.md) | 10 |  | BASE TABLE |
| [codes.type_of_plan_regulation](codes.type_of_plan_regulation.md) | 10 |  | BASE TABLE |
| [codes.type_of_source_data](codes.type_of_source_data.md) | 10 |  | BASE TABLE |
| [codes.type_of_underground](codes.type_of_underground.md) | 10 |  | BASE TABLE |
| [codes.type_of_verbal_plan_regulation](codes.type_of_verbal_plan_regulation.md) | 10 |  | BASE TABLE |
| [codes.type_of_document](codes.type_of_document.md) | 10 |  | BASE TABLE |
| [codes.administrative_region](codes.administrative_region.md) | 10 |  | BASE TABLE |
| [codes.type_of_plan_regulation_group](codes.type_of_plan_regulation_group.md) | 10 |  | BASE TABLE |
| [codes.plan_theme](codes.plan_theme.md) | 10 |  | BASE TABLE |

## Relations

![er](viewpoint-0.svg)

---

> Generated by [tbls](https://github.com/k1LoW/tbls)
