# Customization Guide

This guide explains how to modify the Study Resource Recommender system without writing code. All customizations are done by editing simple JSON files!

## Understanding JSON Format

JSON is a simple text format for storing data. Here's what you need to know:

```json
{
    "key": "value",
    "number": 42,
    "list": ["item1", "item2"],
    "nested": {
        "inner_key": "inner_value"
    }
}
```

**Important rules:**
- Use double quotes `"` (not single quotes)
- Commas separate items (but no comma after the last item)
- Curly braces `{}` hold objects
- Square brackets `[]` hold lists

## Customizing Resources

### File Location
`data/resources.json`

### Adding a New Resource

Open `data/resources.json` in a text editor and add a new entry to the list. Here's an example:

```json
{
    "id": "res_009",
    "title": "Introduction to Data Science",
    "type": "course",
    "subject": "data science",
    "difficulty": "intermediate",
    "format": "video",
    "duration_hours": 40,
    "url": "https://example.com/data-science-course",
    "tags": ["data", "statistics", "python"]
}
```

**Field explanations:**
- `id`: Unique identifier (must start with "res_" and be different from all others)
- `title`: Name of the resource
- `type`: One of: `book`, `video`, `course`
- `subject`: Topic area (e.g., "programming", "mathematics", "science")
- `difficulty`: One of: `beginner`, `intermediate`, `advanced`
- `format`: One of: `text`, `video`
- `duration_hours`: Estimated hours to complete
- `url`: Link to the resource
- `tags`: List of keywords describing the resource

### Removing a Resource

Simply delete the entire resource entry (including the curly braces).

### Editing an Existing Resource

Change any field value. For example, to update the difficulty:

```json
"difficulty": "beginner"  // Changed from "intermediate"
```

## Customizing Recommendation Rules

### File Location
`data/rules.json`

### Understanding the Rules

```json
{
    "weights": {
        "subject_match": 40,
        "difficulty_match": 30,
        "format_preference": 20,
        "tag_match": 10
    },
    "difficulty_progression": {
        "beginner": ["beginner", "intermediate"],
        "intermediate": ["intermediate", "advanced"],
        "advanced": ["advanced"]
    },
    "minimum_score_threshold": 30
}
```

### Weights Explanation

The weights determine how important each factor is when calculating recommendation scores. They should add up to 100.

| Weight | Meaning | Example |
|--------|---------|---------|
| `subject_match` | How much to care about matching the user's subject | If user wants "programming", programming resources get more points |
| `difficulty_match` | How much to care about difficulty level | If user is "beginner", beginner resources get more points |
| `format_preference` | How much to care about video vs text | If user prefers "video", video resources get more points |
| `tag_match` | How much to care about matching tags | If user wants ["python"], resources with "python" tag get points |

### Changing Weights

To make the system care more about difficulty and less about subject:

```json
"weights": {
    "subject_match": 20,      // Reduced from 40
    "difficulty_match": 50,   // Increased from 30
    "format_preference": 20,
    "tag_match": 10
}
```

**Remember:** All weights should add up to 100!

### Difficulty Progression

This controls what difficulty levels are recommended based on the user's current level.

**Default behavior:**
- Beginners see: beginner and intermediate resources
- Intermediate users see: intermediate and advanced resources
- Advanced users see: only advanced resources

**To change this:**

If you want beginners to ONLY see beginner resources:
```json
"difficulty_progression": {
    "beginner": ["beginner"],  // Changed from ["beginner", "intermediate"]
    "intermediate": ["intermediate", "advanced"],
    "advanced": ["advanced"]
}
```

Or if you want advanced users to see all levels:
```json
"difficulty_progression": {
    "beginner": ["beginner", "intermediate"],
    "intermediate": ["intermediate", "advanced"],
    "advanced": ["beginner", "intermediate", "advanced"]  // All levels
}
```

### Minimum Score Threshold

This is the minimum score (out of 100) that a resource must have to be recommended.

- **Default: 30** - Recommends resources that are at least 30% relevant
- **Higher value (e.g., 50)** - Only recommends very strong matches
- **Lower value (e.g., 10)** - Recommends more resources, even weak matches

```json
"minimum_score_threshold": 50  // Only show very good matches
```

## Adding New Subjects

To add a new subject (like "history" or "art"):

1. Add resources with that subject in `data/resources.json`:
   ```json
   "subject": "history"
   ```

2. The system will automatically recognize it!

## Adding New Tags

Tags are flexible - you can add any tag to a resource:

```json
"tags": ["python", "beginner-friendly", "interactive", "free"]
```

Users can then search for resources with these tags.

## Example Customizations

### Make the System More Strict
Only recommend resources that are a very good match:

```json
"weights": {
    "subject_match": 60,
    "difficulty_match": 30,
    "format_preference": 10,
    "tag_match": 0
},
"minimum_score_threshold": 60
```

### Make the System More Flexible
Recommend more resources, even if they're not a perfect match:

```json
"weights": {
    "subject_match": 20,
    "difficulty_match": 20,
    "format_preference": 30,
    "tag_match": 30
},
"minimum_score_threshold": 10
```

### Prioritize Video Learning
Make video resources more likely to be recommended:

```json
"weights": {
    "subject_match": 30,
    "difficulty_match": 30,
    "format_preference": 40,  // Increased
    "tag_match": 0
}
```

## Testing Your Changes

After making changes to `data/resources.json` or `data/rules.json`:

1. **Web Interface:** Refresh your browser (press F5 or Ctrl+R)
2. **CLI:** Restart the application
3. Try getting new recommendations to see how your changes affect the results

## Common Mistakes to Avoid

1. **Forgetting commas** - Each item in a list needs a comma (except the last one)
2. **Using single quotes** - Always use double quotes `"` in JSON
3. **Duplicate IDs** - Each resource must have a unique ID
4. **Weights not adding to 100** - Check your math!
5. **Invalid difficulty levels** - Use only: `beginner`, `intermediate`, `advanced`
6. **Invalid types** - Use only: `book`, `video`, `course`
7. **Invalid formats** - Use only: `text`, `video`

## Reverting Changes

If you make a mistake:
1. The original files are in the project folder
2. You can always restore them from a backup
3. Or manually undo your changes

## Advanced: Understanding the Scoring Algorithm

The system calculates a score for each resource (0-100) based on these factors:

```
Score = (subject_match × 0.40) + (difficulty_match × 0.30) + 
         (format_match × 0.20) + (tag_match × 0.10)
```

Each factor is either 0 (no match) or 1 (match), then multiplied by its weight.

For example, if a resource matches the subject and difficulty but not the format:
```
Score = (1 × 40) + (1 × 30) + (0 × 20) + (0 × 10) = 70
```

If the minimum threshold is 30, this resource would be recommended!
