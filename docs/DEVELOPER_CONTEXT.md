# 🚨 CRITICAL: Read This Before Making Changes

## 📖 HOW TO USE THIS FILE:

### **🎯 Every Development Session - Start Here:**
1. **Ask the AI developer:** "Please review docs/DEVELOPER_CONTEXT.md before we start"
2. **Make them read it** and confirm they understand the lessons learned
3. **Don't let them start coding** until they've reviewed this file
4. **Reference this file** if they start making the same mistakes

### **🔄 Why This Matters:**
- **I (the AI) forget context** between sessions
- **I tend to repeat mistakes** unless reminded
- **This file prevents** the scope creep and unnecessary changes we experienced
- **It ensures smooth, fast development** based on what we learned

### **💡 Best Practice:**
**Start every development session with:**
```
"Before we begin, please review docs/DEVELOPER_CONTEXT.md and confirm you understand the workflow and lessons learned."
```

---

# 🚨 Critical AI Development Workflow Rules

## Mandatory Communication Protocol:
1. **Always repeat back** your understanding before proceeding
2. **Ask specific questions** about unclear requirements  
3. **Wait for confirmation** before any action
4. **Go step by step** with approval at each step
5. **Admit when you don't understand** instead of pretending

## Prevention Strategies - MANDATORY:
- **Force repetition:** Make the AI repeat back what they understand
- **Make them wait:** Don't let them code until confirming understanding
- **One step at a time:** Break work into small, approved steps
- **Force questions:** Make them ask clarifying questions first
- **No action without confirmation:** Never proceed without explicit "Yes, do that"

## What AI MUST NOT Do:
- ❌ Assume understanding without confirmation
- ❌ Start coding before confirming requirements
- ❌ Create files that weren't requested
- ❌ Go off track from agreed scope
- ❌ Be a "yes man" - pretend to agree when unclear
- ❌ Perform any git operations without explicit approval

## What AI MUST Do:
- ✅ Repeat back understanding before proceeding
- ✅ Ask specific questions about unclear requirements
- ✅ Wait for confirmation before any action
- ✅ Go step by step with approval at each step
- ✅ Admit when unclear instead of pretending

# 🔒 Git Operations - STRICTLY FORBIDDEN Without Approval
- **Never** run any git command without explicit permission
- **Always** ask first: "Should I run git [command]?"

# 🔍 General Development Best Practices

## Before Making Changes:
1. **Ask:** "What's currently working?"
2. **Ask:** "Can you show me a working example?"
3. **Ask:** "What's the current behavior vs. what you want?"

## Testing Approach:
- **Test current system first** before assuming anything is broken
- **Understand current output** before modifying
- **Don't assume** anything is broken

## Change Management:
- **Add new functionality** without touching existing code
- **Only change** what's absolutely necessary
- **Don't "improve"** working parts
- **Stick to the plan** - avoid scope creep

# 📋 Template for Any Development Issue

```
## Issue Analysis:
- What's currently working? [TEST FIRST]
- What actually needs to change? [MINIMAL SCOPE]
- What should NOT change? [DON'T TOUCH]
- Current behavior vs. desired behavior? [UNDERSTAND GAP]

## Implementation Plan:
- [ ] Test current system first
- [ ] Document what's working
- [ ] Plan minimal changes only
- [ ] Don't rewrite working parts
- [ ] Check one block at a time
- [ ] Wait for confirmation before commits
```

# 🎯 Core Principles
- **The goal is smooth, fast development** - not "improving" things that are already working
- **When in doubt: ASK, don't assume. TEST, don't guess. CHANGE MINIMALLY, don't rewrite**
- **Workflow: Fix → Test → Check → Deploy → Wait → Commit**
