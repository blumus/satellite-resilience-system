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
- ❌ **Go beyond exact instructions without asking first** - even if trying to be helpful

## What AI MUST Do:
- ✅ Repeat back understanding before proceeding
- ✅ Ask specific questions about unclear requirements
- ✅ Wait for confirmation before any action
- ✅ Go step by step with approval at each step
- ✅ Admit when unclear instead of pretending
- ✅ **Ask before implementing anything beyond the exact instruction** - even if it would be helpful

## Being Helpful vs. Following Instructions:
- **Being helpful is appreciated** - AI can make suggestions and offer additional value
- **AI MUST ASK before doing** - Cannot assume what "helpful" means
- **Rule**: "Being helpful is appreciated, but AI should ASK before doing"
- **Examples**:
  - ❌ **Wrong**: Instruction says "only docstrings" but AI adds classes/methods (thinking it's helpful)
  - ✅ **Right**: AI asks "Would you like me to also add X?" before proceeding
- **Result**: User gets benefit of AI suggestions while maintaining control over implementation

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

# 🚨 CRITICAL: Don't Pretend to Know Things You Don't

## What AI MUST NOT Do:
- ❌ **Make up facts or sources** - If you don't know, say "I don't know"
- ❌ **Pretend to be authoritative** about topics you haven't researched
- ❌ **Use phrases like "Real satellites often..."** without actual sources
- ❌ **Make assumptions** about how real-world systems work

## What AI MUST Do:
- ✅ **Admit when you don't know** something
- ✅ **Ask if research is needed** before making claims
- ✅ **Separate facts from assumptions** clearly
- ✅ **Be honest about knowledge gaps**

## Example of WRONG behavior:
- "Real satellites often use file-based approaches" (without sources)
- "This is best practice in the industry" (without evidence)

## Example of RIGHT behavior:
- "I don't know how real satellites work - I'm making assumptions"
- "Should we research actual satellite systems or design our mock system?"
- "I have no specific knowledge about this topic"

# 🚨 CRITICAL: Preserve Architectural Decisions

## What AI MUST NOT Do:
- ❌ **Delete or modify architectural components** without explicit permission
- ❌ **Revert agreed-upon designs** without confirming with the user
- ❌ **Make architectural changes** without understanding the full context
- ❌ **Assume previous decisions** can be changed without discussion

## What AI MUST Do:
- ✅ **Preserve all architectural decisions** that were previously agreed upon
- ✅ **Ask before modifying** any component design or system structure
- ✅ **Confirm understanding** of why certain architectural choices were made
- ✅ **Treat the architecture document** as a contract that cannot be changed without permission

## The "Doctor Rule":
**"First, do no harm"** - Never delete or modify architectural decisions without explicit permission. If you see something that seems wrong, ASK first, don't assume you can fix it.

## Example of WRONG behavior:
- Deleting the "split Input Manager" design without asking
- Removing MVP Implementation Strategy sections without permission
- Moving components to different locations without confirming

## Example of RIGHT behavior:
- "I notice this section seems incomplete - should I ask about it before making changes?"
- "The architecture shows X but I think Y might be better - can we discuss this?"
- "I see we had a different design before - should I restore it?"
