# Content Template Pattern for Kintsugi Docs

**Purpose**: Standardized template for all content-oriented pages (non-API reference)  
**Usage**: Copy this pattern for guides, tutorials, integration docs, etc.

---

## 🎨 Modern Content Pattern

### Page Structure Template

```markdown
---
title: "Page Title"
description: "Brief description for SEO and navigation"
---

# Page Title

<Note>
**Welcome message or key insight** - Brief, engaging introduction to the topic.
</Note>

Brief paragraph explaining what this page covers and why it's important.

<CardGroup cols={2}>
  <Card title="Quick Action" icon="rocket" href="#quick-action">
    Primary action users want to take
  </Card>
  <Card title="Related Guide" icon="book" href="/docs/related">
    Link to related content
  </Card>
  <Card title="API Reference" icon="code" href="/reference/endpoint">
    Link to relevant API docs
  </Card>
  <Card title="Support" icon="headset" href="https://trykintsugi.com/support">
    Get help if needed
  </Card>
</CardGroup>

## Main Section Title

<Steps>
  <Step title="Step Title">
    <AccordionGroup>
      <Accordion title="Sub-topic 1">
        Content for sub-topic 1
        
        <Tabs>
          <Tab title="Option A">
            Content for option A
          </Tab>
          <Tab title="Option B">
            Content for option B
          </Tab>
        </Tabs>
      </Accordion>
      
      <Accordion title="Sub-topic 2">
        Content for sub-topic 2
        
        <Note>
          Additional context or tips
        </Note>
      </Accordion>
    </AccordionGroup>
  </Step>
  
  <Step title="Next Step Title">
    <!-- Repeat pattern -->
  </Step>
</Steps>

## Related Actions

<CardGroup cols={3}>
  <Card title="Action 1" icon="icon-name" href="/link">
    Description of action
  </Card>
  <Card title="Action 2" icon="icon-name" href="/link">
    Description of action
  </Card>
  <Card title="Action 3" icon="icon-name" href="/link">
    Description of action
  </Card>
</CardGroup>

## Need Help?

<AccordionGroup>
  <Accordion title="Common Questions">
    <Tabs>
      <Tab title="Category 1">
        - Question 1: Answer
        - Question 2: Answer
        - Question 3: Answer
      </Tab>
      <Tab title="Category 2">
        - Question 1: Answer
        - Question 2: Answer
      </Tab>
    </Tabs>
  </Accordion>
  
  <Accordion title="Get Support">
    <CardGroup cols={2}>
      <Card title="Email Support" icon="mail" href="mailto:support@trykintsugi.com">
        Get help from our team
      </Card>
      <Card title="Live Chat" icon="message-circle" href="https://trykintsugi.com/support">
        Chat with us
      </Card>
    </CardGroup>
  </Accordion>
</AccordionGroup>
```

---

## 🧩 Component Usage Guide

### Interactive Components

**AccordionGroup + Accordion**: For collapsible sections
```markdown
<AccordionGroup>
  <Accordion title="Click to expand">
    Content inside accordion
  </Accordion>
</AccordionGroup>
```

**Tabs**: For multiple options/approaches
```markdown
<Tabs>
  <Tab title="Option 1">
    Content for option 1
  </Tab>
  <Tab title="Option 2">
    Content for option 2
  </Tab>
</Tabs>
```

**Steps**: For sequential processes
```markdown
<Steps>
  <Step title="Step 1">
    Content for step 1
  </Step>
  <Step title="Step 2">
    Content for step 2
  </Step>
</Steps>
```

### Callout Components

**Note**: General information
```markdown
<Note>
Important information or context
</Note>
```

**Tip**: Helpful suggestions
```markdown
<Tip>
Pro tip or helpful suggestion
</Tip>
```

**Warning**: Important warnings
```markdown
<Warning>
Critical information or warnings
</Warning>
```

**Check**: Success/confirmation
```markdown
<Check>
Success message or confirmation
</Check>
```

**Info**: Additional context
```markdown
<Info>
Additional context or background info
</Info>
```

### Navigation Components

**CardGroup**: For related actions/links
```markdown
<CardGroup cols={2}>
  <Card title="Title" icon="icon-name" href="/link">
    Description
  </Card>
</CardGroup>
```

---

## 📝 Writing Guidelines

### Content Structure
1. **Start with engaging intro** - Use Note component
2. **Provide quick actions** - Use CardGroup at top
3. **Break into logical steps** - Use Steps component
4. **Use accordions for details** - Keep main flow clean
5. **End with related actions** - Use CardGroup
6. **Include help section** - Use AccordionGroup

### Writing Style
- **Clear and concise** - Respect user's time
- **Action-oriented** - Focus on what users can do
- **Scannable** - Use headers, lists, callouts
- **Progressive disclosure** - Hide complexity in accordions

### Visual Hierarchy
- **H1**: Page title only
- **H2**: Main sections
- **H3**: Subsections (use sparingly)
- **Use components** instead of more headers

---

## 🎯 Page Types & Examples

### Getting Started Pages
- Use Steps for onboarding flow
- Use AccordionGroup for detailed options
- Use CardGroup for quick actions

### Integration Guides
- Use Tabs for different platforms
- Use Steps for setup process
- Use AccordionGroup for configuration options

### Tutorial Pages
- Use Steps for tutorial flow
- Use Tabs for different approaches
- Use Note/Tip for helpful hints

### Troubleshooting Pages
- Use AccordionGroup for different issues
- Use Tabs for different solutions
- Use Warning for critical issues

---

## ✅ Quality Checklist

Before publishing any content page:

- [ ] **Engaging intro** with Note component
- [ ] **Quick actions** with CardGroup at top
- [ ] **Logical flow** with Steps component
- [ ] **Progressive disclosure** with AccordionGroup
- [ ] **Related actions** with CardGroup at bottom
- [ ] **Help section** with AccordionGroup
- [ ] **Consistent styling** throughout
- [ ] **Working links** (test all href attributes)
- [ ] **Proper icons** (use Font Awesome names)
- [ ] **Mobile responsive** (test on mobile)

---

## 🚀 Quick Start

1. **Copy the template** above
2. **Replace placeholders** with your content
3. **Choose appropriate components** for your content type
4. **Test locally** with `mintlify dev`
5. **Review checklist** before publishing

---

**This template ensures all your content pages have a modern, interactive, and consistent feel!**
