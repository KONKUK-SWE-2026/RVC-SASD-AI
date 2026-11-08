---
name: sa-process-specification
description: Incrementally generate and refine Process Specifications after each DFD level (0-3), preserving existing definitions and maintaining consistency with requirements and the Data Dictionary.
---

# Process Specification Generation

## Inputs
### Required: Current Analysis Inputs
- preliminary_requirements.md
- artifacts/SA/event_list.md
- artifacts/SA/context_diagram.md
- artifacts/SA/DFD/dfd_level_<N>.md (the newly generated DFD level, N = 0, 1, 2, or 3)
- artifacts/SA/data_dictionary.md (the current version reflecting the same DFD level)

### Existing Artifact (if available)
- artifacts/SA/process_specification.md

### Reference Template
- templates/process-specification.md

### Preconditions
- Run incrementally after each DFD level (0-3) is generated.
- Use the current DFD to identify processes, numbering, parent-child relationships,
  and interfaces; use the Data Dictionary for named flow and store definitions.
- At Level 0, initialize Process Specifications if no previous file exists.
- At Levels 1-3, read and preserve existing specifications before appending
  or refining the specifications for the current level.
- Do not use the Level 4 FSM as a process to be separately specified.
- Report missing dependencies and inconsistencies without inventing behavior.

## Objective
Describe the detailed behavior of every
process defined in DFD Levels 0 through 3.

Do not generate a separate Process Specification
for the Level 4 Controller FSM.


## Procedure

### Step 1. Identify Processes
1. Read the newly generated DFD level.
2. Read the existing Process Specifications (if available).
3. Identify newly introduced processes and their numbers.
4. Identify parent-child relationships.
5. Identify all input and output flows.

### Step 2. Analyze Process Behavior
For each process:
1. Identify its purpose.
2. Identify input data and control signals.
3. Identify output data and control signals.
4. Determine the processing logic.
5. Identify execution conditions and triggering events.
6. Identify interactions with Data Stores.

### Step 3. Generate or Update Process Specifications
1. Initialize Process Specifications if they do not exist.
2. Add specifications for newly introduced processes.
3. Refine existing specifications when additional details become available.
4. Preserve previously documented specifications.
5. Save the updated Process Specifications.

For each process, document:
- Process ID
- Process Name
- Parent Process
- Purpose
- Inputs
- Outputs
- Trigger or Execution Condition
- Processing Logic
- Relevant Requirements

### Step 4. Validate Hierarchical Consistency
1. Verify that each child process refines its parent process.
2. Verify that process inputs and outputs match the DFD.
3. Verify consistency with the Data Dictionary.
4. Verify consistency with the preliminary requirements.


## Guidelines
- Update Process Specifications after each DFD level (0-3).
- Preserve existing specifications during incremental updates.
- Use the same process names and numbers as the DFD.
- Describe processing logic explicitly, using pseudocode when appropriate.
- Maintain traceability to the preliminary requirements.
- Do not invent unspecified behavior.
- Report missing or ambiguous requirements.
- Do not generate Process Specifications for the Level 4 Controller FSM.


## Formatting
Follow templates/process-specification.md.


## Validation
- Every process in the generated DFD Levels 0-3 must have a corresponding specification.
- Process IDs, names, inputs, and outputs must match the DFD.
- Child process behavior must be consistent with its parent process.
- Processing logic must be consistent with the requirements and Data Dictionary.
- No existing process specifications may be lost during an update.


## Output
- artifacts/SA/process_specification.md
