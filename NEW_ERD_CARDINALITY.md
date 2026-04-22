# SEAIT TechnoPath - Entity Relationship Diagram (ERD)

## Overview
This document contains the complete ERD and cardinality analysis for the SEAIT TechnoPath Campus Guide system.

**Total Entities:** 22 main tables
**Database:** PostgreSQL (via Django ORM)

---

## Entity Relationship Diagram (Text Format)

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   Department    │       │   AdminUser     │       │ NotificationType│
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ PK id           │       │ PK id           │       │ PK id           │
│ name            │◄──────┤ username        │       │ name            │
│ code (unique)   │  0..1 │ email           │       │ description     │
│ description     │       │ display_name    │       │ icon_name       │
│ is_active       │       │ role            │──────►│ color_hex       │
│ created_at      │       │ department      │  0..* │ is_active       │
└─────────────────┘       │ is_active       │       └─────────────────┘
         │                │ login_attempts  │              │
         │                │ locked_until    │              │
         │                │ created_at      │              │
         │                └─────────────────┘              │
         │                        │                       │
         │     ┌──────────────────┼──────────────────┐    │
         │     │                  │                  │    │
         ▼     ▼                  ▼                  ▼    ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────┐
│    Facility     │    │  Announcement   │    │NotificationPreference│
├─────────────────┤    ├─────────────────┤    ├─────────────────────┤
│ PK id           │    │ PK id           │    │ PK id               │
│ FK department   │◄───┤ FK created_by   │◄───┤ FK user             │◄──┐
│ name            │0..1│ FK approved_by  │◄──┐│ FK notification_type│◄──┼┐
│ code (unique)   │    │ FK rejected_by  │◄─┼┘│ is_enabled          │   ││
│ description     │    │ FK archived_by  │◄─┼┘ └─────────────────────┘   ││
│ facility_type   │    │ title           │  │                             ││
│ building_code   │    │ content         │  │    ┌─────────────────┐     ││
│ latitude        │    │ source_label    │  │    │  Notification   │     ││
│ longitude       │    │ source_color    │  │    ├─────────────────┤     ││
│ image_path      │    │ scope           │  │    │ PK id           │     ││
│ map_svg_id      │    │ target_dept     │  └───►│ FK announcement │◄────┘│
│ total_floors    │    │ target_users    │       │ FK created_by   │◄─────┘
│ is_deleted      │    │ status          │       │ title           │
│ is_active       │    │ requires_approval│      │ message         │
└────────┬────────┘    │ rejection_note  │       │ type            │
         │              │ is_deleted      │       │ source_label    │
         │              │ created_at      │       │ source_color    │
         │              │ approved_at     │       │ priority        │
         │              │ archived_at     │       │ is_read         │
         │              └─────────────────┘       │ expires_at      │
         │                                          │ created_at      │
         │                                          └────────┬────────┘
         │                                                   │
         │                                          ┌────────▼────────┐
         │                                          │NotificationReadStatus
         │                                          ├─────────────────┤
         │                                          │ PK id           │
         │                                          │ FK user         │◄──┐
         │                                          │ FK notification │◄──┼┐
         │                                          │ read_at         │   ││
         │                                          └─────────────────┘   ││
         │                                              unique: [user,    ││
         │                                                      notification]││
         │                                                                  ││
         │         ┌─────────────────┐    ┌─────────────────┐              ││
         │         │      Room       │    │   MapMarker     │              ││
         │         ├─────────────────┤    ├─────────────────┤              ││
         │         │ PK id           │    │ PK id           │              ││
         └────────►│ FK facility     │◄───┤ FK facility     │◄─────────────┘│
         1..*      │ name            │1..*│ FK room         │◄─────────────┘
                   │ code            │    │ name            │ 0..1
                   │ room_number     │    │ x_position      │
                   │ description     │    │ y_position      │
                   │ floor           │    │ marker_type     │
                   │ map_svg_id      │    │ icon_name       │
                   │ room_type       │    │ color_hex       │
                   │ capacity        │    │ is_active       │
                   │ is_office       │    │ created_at      │
                   │ is_crucial      │    └─────────────────┘
                   │ search_count    │           │
                   │ is_deleted      │           │
                   │ is_active       │           │
                   └────────┬────────┘           │
                            │                     │
                            │         ┌───────────┘
                            │         │
                            ▼         ▼
                   ┌─────────────────┐    ┌─────────────────┐
                   │  NavigationNode │    │    MapLabel     │
                   ├─────────────────┤    ├─────────────────┤
                   │ PK id           │    │ PK id           │
                   │ FK facility     │◄───┤ label_text      │
                   │ FK room         │◄──┐│ x_position      │
                   │ name            │   ││ y_position      │
                   │ node_type       │   ││ font_size       │
                   │ map_svg_id      │   ││ color_hex       │
                   │ x, y            │   ││ rotation        │
                   │ floor           │   ││ is_active       │
                   │ is_deleted      │   ││ created_at      │
                   └────────┬────────┘   │└─────────────────┘
                            │            │
                            │    ┌───────┘
                            │    │
                            ▼    ▼
                   ┌─────────────────┐    ┌─────────────────┐
                   │ NavigationEdge  │    │     Path        │
                   ├─────────────────┤    ├─────────────────┤
                   │ PK id           │    │ PK id           │
                   │ FK from_node    │◄───┤ FK facility     │◄──┐
                   │ FK to_node      │◄───┤ FK room         │◄─┐│
                   │ distance        │ 1..*│ name            │  ││
                   │ is_bidirectional│    │ description     │  ││
                   │ is_deleted      │    │ FK created_by   │◄─┼┘│
                   └─────────────────┘    │ floor           │  ││
                                            │ is_deleted      │  ││
                                            │ created_at      │  ││
                                            └────────┬────────┘  ││
                                                     │           ││
                                                     ▼           ││
                                            ┌─────────────────┐  ││
                                            │   PathPoint     │  ││
                                            ├─────────────────┤  ││
                                            │ PK id           │  ││
                                            │ FK path         │◄─┼┘
                                            │ sequence        │  │
                                            │ element_id      │  │
                                            │ x, y            │  │
                                            │ is_deleted      │  │
                                            └─────────────────┘  │
                                                                   │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┤
│    FAQEntry     │    │  AIChatLog      │    │    Feedback     │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ PK id           │◄───┤ FK faq_entry    │◄─┐│ PK id           │
│ question        │ 0..1│ user_query      │  ││ rating          │
│ answer          │    │ ai_response     │  ││ comment         │
│ category        │    │ mode            │  ││ category        │
│ keywords        │    │ response_time_ms│  ││ FK facility     │◄──┐
│ usage_count     │    │ is_successful   │  ││ FK room         │◄──┼┐
│ is_deleted      │    │ error_message   │  ││ is_anonymous    │   ││
│ created_at      │    │ session_id      │  ││ location        │   ││
└─────────────────┘    │ created_at      │  ││ is_flagged      │   ││
         ▲             └─────────────────┘  ││ flag_reason     │   ││
         │                                   ││ created_at      │   ││
         │             ┌─────────────────┐   │└─────────────────┘   ││
         │             │  FAQSuggestion  │   │                     ││
         │             ├─────────────────┤   │                     ││
         │             │ PK id           │   │                     ││
         └─────────────┤ FK faq_entry    │◄──┘                     ││
           0..1         │ FK reviewed_by  │◄────────────────────────┘│
                       │ suggested_q     │                          │
                       │ suggested_a     │                          │
                       │ category        │                          │
                       │ keywords        │                          │
                       │ source_queries  │                          │
                       │ query_count     │                          │
                       │ confidence_score│                          │
                       │ status          │                          │
                       │ review_note     │                          │
                       │ created_at      │                          │
                       └─────────────────┘                          │
                                                                    │
┌─────────────────┐    ┌─────────────────┐                          │
│ AdminAuditLog   │    │  SearchHistory  │                          │
├─────────────────┤    ├─────────────────┤                          │
│ PK id           │    │ PK id           │                          │
│ FK admin        │◄───┤ FK user         │◄─────────────────────────┘
│ action          │    │ query           │
│ entity_type     │    │ results_count   │
│ entity_id       │    │ was_clicked     │
│ entity_label    │    │ created_at      │
│ old_value_json  │    └─────────────────┘
│ new_value_json  │
│ ip_address      │
│ created_at      │
└─────────────────┘

┌─────────────────┐
│    AppConfig    │
├─────────────────┤
│ PK id           │
│ config_key (U)  │
│ config_value    │
│ description     │
│ FK updated_by   │◄────────────────┐
│ updated_at      │                 │
└─────────────────┘                 │
                                    │
                         ┌──────────┴──────────┐
                         │     AdminUser       │
                         │  (referenced by)    │
                         └─────────────────────┘
```

---

## Cardinality Summary Table

| Relationship | From Entity | To Entity | Cardinality | Description |
|--------------|-------------|-----------|-------------|-------------|
| **Department → AdminUser** | `Department.head_user` | `AdminUser` | **0..1 : 0..*** | Department may have 0 or 1 head user; an admin may head 0 or many departments |
| **AdminUser → Department** | `AdminUser.department` | `Department` | **0..* : 0..1** | Admin may belong to 0 or 1 department; a department can have many admins |
| **Facility → Department** | `Facility.department` | `Department` | **0..* : 0..1** | Facility may belong to 0 or 1 department |
| **Room → Facility** | `Room.facility` | `Facility` | **1..* : 1** | Room belongs to exactly 1 facility; a facility has 1 or many rooms |
| **MapMarker → Facility** | `MapMarker.facility` | `Facility` | **0..* : 0..1** | Map marker may reference 0 or 1 facility |
| **MapMarker → Room** | `MapMarker.room` | `Room` | **0..* : 0..1** | Map marker may reference 0 or 1 room |
| **NavigationNode → Facility** | `NavigationNode.facility` | `Facility` | **0..* : 0..1** | Nav node may reference 0 or 1 facility |
| **NavigationNode → Room** | `NavigationNode.room` | `Room` | **0..* : 0..1** | Nav node may reference 0 or 1 room |
| **NavigationEdge → NavigationNode** | `NavigationEdge.from_node` | `NavigationNode` | **1..* : 1** | Edge originates from exactly 1 node |
| **NavigationEdge → NavigationNode** | `NavigationEdge.to_node` | `NavigationNode` | **1..* : 1** | Edge connects to exactly 1 node |
| **Path → Facility** | `Path.facility` | `Facility` | **0..* : 0..1** | Path may reference 0 or 1 facility |
| **Path → Room** | `Path.room` | `Room` | **0..* : 0..1** | Path may reference 0 or 1 room |
| **Path → AdminUser** | `Path.created_by` | `AdminUser` | **0..* : 0..1** | Path may be created by 0 or 1 admin |
| **PathPoint → Path** | `PathPoint.path` | `Path` | **1..* : 1** | Path point belongs to exactly 1 path |
| **Feedback → Facility** | `Feedback.facility` | `Facility` | **0..* : 0..1** | Feedback may reference 0 or 1 facility |
| **Feedback → Room** | `Feedback.room` | `Room` | **0..* : 0..1** | Feedback may reference 0 or 1 room |
| **FAQEntry → AIChatLog** | `AIChatLog.faq_entry` | `FAQEntry` | **0..* : 0..1** | Chat log may reference 0 or 1 FAQ |
| **FAQEntry → FAQSuggestion** | `FAQSuggestion.faq_entry` | `FAQEntry` | **0..1 : 0..1** | Suggestion may be converted to 0 or 1 FAQ |
| **FAQSuggestion → AdminUser** | `FAQSuggestion.reviewed_by` | `AdminUser` | **0..* : 0..1** | Suggestion may be reviewed by 0 or 1 admin |
| **Announcement → AdminUser** | `Announcement.created_by` | `AdminUser` | **0..* : 0..1** | Created by 0 or 1 admin (SET_NULL) |
| **Announcement → AdminUser** | `Announcement.approved_by` | `AdminUser` | **0..* : 0..1** | Approved by 0 or 1 admin |
| **Announcement → AdminUser** | `Announcement.rejected_by` | `AdminUser` | **0..* : 0..1** | Rejected by 0 or 1 admin |
| **Announcement → AdminUser** | `Announcement.archived_by` | `AdminUser` | **0..* : 0..1** | Archived by 0 or 1 admin |
| **Notification → Announcement** | `Notification.announcement` | `Announcement` | **0..* : 0..1** | Notification may reference 0 or 1 announcement |
| **Notification → AdminUser** | `Notification.created_by` | `AdminUser` | **0..* : 0..1** | Created by 0 or 1 admin |
| **NotificationReadStatus → Notification** | `NotificationReadStatus.notification` | `Notification` | **1 : 1** | Read status belongs to exactly 1 notification |
| **NotificationReadStatus → AdminUser** | `NotificationReadStatus.user` | `AdminUser` | **1 : 1** | Read status belongs to exactly 1 user |
| **NotificationPreference → AdminUser** | `NotificationPreference.user` | `AdminUser` | **1 : 1** | Preference belongs to exactly 1 user |
| **NotificationPreference → NotificationType** | `NotificationPreference.notification_type` | `NotificationType` | **1 : 1** | Preference belongs to exactly 1 type |
| **AdminAuditLog → AdminUser** | `AdminAuditLog.admin` | `AdminUser` | **0..* : 0..1** | Log entry may reference 0 or 1 admin |
| **SearchHistory → AdminUser** | `SearchHistory.user` | `AdminUser` | **0..* : 0..1** | Search may be by 0 or 1 admin |
| **AppConfig → AdminUser** | `AppConfig.updated_by` | `AdminUser` | **0..* : 0..1** | Config may be updated by 0 or 1 admin |

---

## Entity Definitions

### 1. Department
```
┌─────────────────┐
│   Department    │
├─────────────────┤
│ PK id (bigint)  │
│ name (varchar)  │
│ code (varchar)  │ ← unique
│ description     │
│ FK head_user    │ → AdminUser
│ is_active       │
│ created_at      │
└─────────────────┘
```

### 2. AdminUser
```
┌─────────────────┐
│   AdminUser     │
├─────────────────┤
│ PK id (bigint)  │
│ username        │ ← unique
│ email           │
│ display_name    │
│ role            │ ← choices
│ department      │ → Department
│ department_label│
│ is_active       │
│ login_attempts  │
│ locked_until    │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

### 3. Facility
```
┌─────────────────┐
│    Facility     │
├─────────────────┤
│ PK id (bigint)  │
│ FK department   │ → Department
│ name            │
│ code            │ ← unique
│ description     │
│ facility_type   │ ← choices
│ building_code   │
│ latitude        │
│ longitude       │
│ image_path      │
│ map_svg_id      │
│ total_floors    │
│ is_deleted      │
│ is_active       │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

### 4. Room
```
┌─────────────────┐
│      Room       │
├─────────────────┤
│ PK id (bigint)  │
│ FK facility     │ → Facility (CASCADE)
│ name            │
│ code            │
│ room_number     │
│ description     │
│ floor           │
│ map_svg_id      │
│ room_type       │ ← choices
│ capacity        │
│ is_office       │
│ is_crucial      │
│ search_count    │
│ is_deleted      │
│ is_active       │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

### 5. NavigationNode
```
┌─────────────────┐
│ NavigationNode  │
├─────────────────┤
│ PK id (bigint)  │
│ name            │
│ node_type       │ ← choices
│ FK facility     │ → Facility (SET_NULL)
│ FK room         │ → Room (SET_NULL)
│ map_svg_id      │ ← unique
│ x               │
│ y               │
│ floor           │
│ is_deleted      │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

### 6. NavigationEdge
```
┌─────────────────┐
│ NavigationEdge  │
├─────────────────┤
│ PK id (bigint)  │
│ FK from_node    │ → NavigationNode
│ FK to_node      │ → NavigationNode
│ distance        │
│ is_bidirectional│
│ is_deleted      │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

### 7. Path
```
┌─────────────────┐
│     Path        │
├─────────────────┤
│ PK id (bigint)  │
│ name            │
│ description     │
│ FK facility     │ → Facility (SET_NULL)
│ FK room         │ → Room (SET_NULL)
│ floor           │
│ FK created_by   │ → AdminUser (SET_NULL)
│ is_deleted      │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

### 8. PathPoint
```
┌─────────────────┐
│   PathPoint     │
├─────────────────┤
│ PK id (bigint)  │
│ FK path         │ → Path (CASCADE)
│ sequence        │
│ element_id      │
│ x               │
│ y               │
│ is_deleted      │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

### 9. Announcement
```
┌─────────────────┐
│  Announcement   │
├─────────────────┤
│ PK id (bigint)  │
│ FK created_by   │ → AdminUser (SET_NULL)
│ FK approved_by  │ → AdminUser (SET_NULL)
│ FK rejected_by  │ → AdminUser (SET_NULL)
│ FK archived_by  │ → AdminUser (SET_NULL)
│ title           │
│ content         │
│ source_label    │
│ source_color    │
│ scope           │ ← choices
│ target_department│
│ target_users    │ ← JSON
│ status          │ ← choices
│ requires_approval│
│ rejection_note  │
│ approved_at     │
│ archived_at     │
│ is_deleted      │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

### 10. Notification
```
┌─────────────────┐
│  Notification   │
├─────────────────┤
│ PK id (bigint)  │
│ FK announcement │ → Announcement (SET_NULL)
│ FK created_by   │ → AdminUser (SET_NULL)
│ title           │
│ message         │
│ type            │ ← choices
│ source_label    │
│ source_color    │
│ priority        │
│ is_read         │
│ expires_at      │
│ created_at      │
└─────────────────┘
```

### 11. NotificationType
```
┌─────────────────┐
│ NotificationType│
├─────────────────┤
│ PK id (bigint)  │
│ name            │ ← unique
│ description     │
│ icon_name       │
│ color_hex       │
│ is_active       │
│ created_at      │
└─────────────────┘
```

### 12. NotificationReadStatus
```
┌─────────────────┐
│NotificationRead │
│    Status       │
├─────────────────┤
│ PK id (bigint)  │
│ FK user         │ → AdminUser (CASCADE)
│ FK notification │ → Notification (CASCADE)
│ read_at         │
└─────────────────┘

unique_together: [user, notification]
```

### 13. NotificationPreference
```
┌─────────────────┐
│NotificationPref │
├─────────────────┤
│ PK id (bigint)  │
│ FK user         │ → AdminUser (CASCADE)
│ FK notification_type│ → NotificationType (CASCADE)
│ is_enabled      │
│ created_at      │
└─────────────────┘

unique_together: [user, notification_type]
```

### 14. FAQEntry
```
┌─────────────────┐
│    FAQEntry     │
├─────────────────┤
│ PK id (bigint)  │
│ question        │
│ answer          │
│ category        │ ← choices
│ keywords        │
│ usage_count     │
│ is_deleted      │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

### 15. AIChatLog
```
┌─────────────────┐
│   AIChatLog     │
├─────────────────┤
│ PK id (bigint)  │
│ FK faq_entry    │ → FAQEntry (SET_NULL)
│ user_query      │
│ ai_response     │
│ mode            │ ← choices
│ response_time_ms│
│ is_successful   │
│ error_message   │
│ session_id      │
│ created_at      │
└─────────────────┘
```

### 16. FAQSuggestion
```
┌─────────────────┐
│ FAQSuggestion   │
├─────────────────┤
│ PK id (bigint)  │
│ FK faq_entry    │ → FAQEntry (SET_NULL)
│ FK reviewed_by  │ → AdminUser (SET_NULL)
│ suggested_question│
│ suggested_answer│
│ category        │
│ keywords        │
│ source_queries  │ ← JSON
│ query_count     │
│ confidence_score│
│ status          │ ← choices
│ review_note     │
│ reviewed_at     │
│ created_at      │
│ updated_at      │
└─────────────────┘
```

### 17. Feedback
```
┌─────────────────┐
│    Feedback     │
├─────────────────┤
│ PK id (bigint)  │
│ FK facility     │ → Facility (SET_NULL)
│ FK room         │ → Room (SET_NULL)
│ rating          │
│ comment         │
│ category        │ ← choices
│ is_anonymous    │
│ location        │
│ is_flagged      │
│ flag_reason     │
│ created_at      │
└─────────────────┘
```

### 18. MapMarker
```
┌─────────────────┐
│   MapMarker     │
├─────────────────┤
│ PK id (bigint)  │
│ FK facility     │ → Facility (SET_NULL)
│ FK room         │ → Room (SET_NULL)
│ name            │
│ x_position      │
│ y_position      │
│ marker_type     │ ← choices
│ icon_name       │
│ color_hex       │
│ is_active       │
│ created_at      │
└─────────────────┘
```

### 19. MapLabel
```
┌─────────────────┐
│    MapLabel     │
├─────────────────┤
│ PK id (bigint)  │
│ label_text      │
│ x_position      │
│ y_position      │
│ font_size       │
│ color_hex       │
│ rotation        │
│ is_active       │
│ created_at      │
└─────────────────┘
```

### 20. AdminAuditLog
```
┌─────────────────┐
│ AdminAuditLog   │
├─────────────────┤
│ PK id (bigint)  │
│ FK admin        │ → AdminUser (SET_NULL)
│ action          │ ← choices
│ entity_type     │
│ entity_id       │
│ entity_label    │
│ old_value_json  │
│ new_value_json  │
│ ip_address      │
│ created_at      │
└─────────────────┘
```

### 21. SearchHistory
```
┌─────────────────┐
│  SearchHistory  │
├─────────────────┤
│ PK id (bigint)  │
│ FK user         │ → AdminUser (SET_NULL)
│ query           │
│ results_count   │
│ was_clicked     │
│ created_at      │
└─────────────────┘
```

### 22. AppConfig
```
┌─────────────────┐
│    AppConfig    │
├─────────────────┤
│ PK id (bigint)  │
│ config_key      │ ← unique
│ config_value    │
│ description     │
│ FK updated_by   │ → AdminUser (SET_NULL)
│ updated_at      │
└─────────────────┘
```

---

## Notes

- **Soft Delete Pattern:** Most entities have `is_deleted` field for soft deletion
- **Audit Trail:** `AdminAuditLog` tracks all admin actions for accountability
- **Navigation System:** Uses graph structure (nodes + edges) for pathfinding
- **Multi-Tenancy:** Departments can be isolated through `target_department` fields
- **Notification System:** Supports both in-app and push notifications with read receipts
