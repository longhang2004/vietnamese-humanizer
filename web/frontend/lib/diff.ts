export interface DiffSegment {
  kind: "equal" | "removed" | "added";
  text: string;
}

const MAX_DP_CELLS = 2_250_000;

function tokenize(text: string): string[] {
  if (!text) return [];
  return text.split(/(\s+)/).filter(Boolean);
}

function pushSegment(
  segments: DiffSegment[],
  kind: DiffSegment["kind"],
  text: string,
): void {
  if (!text) return;
  const previous = segments[segments.length - 1];
  if (previous && previous.kind === kind) {
    previous.text += text;
    return;
  }
  segments.push({ kind, text });
}

function flushEditRun(target: DiffSegment[], run: DiffSegment[]): void {
  if (run.length === 0) return;
  const hasEdits = run.some((segment) => segment.kind !== "equal");
  if (!hasEdits) {
    for (const segment of run) {
      pushSegment(target, segment.kind, segment.text);
    }
    return;
  }

  const removedText = run
    .filter((segment) => segment.kind !== "added")
    .map((segment) => segment.text)
    .join("");
  const addedText = run
    .filter((segment) => segment.kind !== "removed")
    .map((segment) => segment.text)
    .join("");

  const minLen = Math.min(removedText.length, addedText.length);
  let lead = 0;
  while (
    lead < minLen &&
    removedText[lead] === addedText[lead] &&
    /\s/.test(removedText[lead])
  ) {
    lead += 1;
  }

  let trail = 0;
  while (
    trail < minLen - lead &&
    removedText[removedText.length - 1 - trail] ===
      addedText[addedText.length - 1 - trail] &&
    /\s/.test(removedText[removedText.length - 1 - trail])
  ) {
    trail += 1;
  }

  if (lead > 0) {
    pushSegment(target, "equal", removedText.slice(0, lead));
  }
  const removedBody = removedText.slice(lead, removedText.length - trail);
  const addedBody = addedText.slice(lead, addedText.length - trail);
  if (removedBody) {
    pushSegment(target, "removed", removedBody);
  }
  if (addedBody) {
    pushSegment(target, "added", addedBody);
  }
  if (trail > 0) {
    pushSegment(target, "equal", removedText.slice(removedText.length - trail));
  }
}

/** Merge whitespace-only equal bridges between edits so replaced phrases stay whole. */
function normalizeEditRuns(segments: DiffSegment[]): DiffSegment[] {
  const normalized: DiffSegment[] = [];
  let run: DiffSegment[] = [];
  for (const segment of segments) {
    const isWordAnchor = segment.kind === "equal" && /\S/.test(segment.text);
    if (isWordAnchor) {
      flushEditRun(normalized, run);
      run = [];
      pushSegment(normalized, "equal", segment.text);
    } else {
      run.push(segment);
    }
  }
  flushEditRun(normalized, run);
  return normalized;
}

function diffSequence(a: string[], b: string[]): DiffSegment[] {
  const segments: DiffSegment[] = [];
  let prefix = 0;
  const minLength = Math.min(a.length, b.length);
  while (prefix < minLength && a[prefix] === b[prefix]) {
    prefix += 1;
  }

  let suffix = 0;
  while (
    suffix < minLength - prefix &&
    a[a.length - 1 - suffix] === b[b.length - 1 - suffix]
  ) {
    suffix += 1;
  }

  for (let index = 0; index < prefix; index += 1) {
    pushSegment(segments, "equal", a[index]);
  }

  const midA = a.slice(prefix, a.length - suffix);
  const midB = b.slice(prefix, b.length - suffix);
  const m = midA.length;
  const n = midB.length;

  if (m === 0 && n > 0) {
    pushSegment(segments, "added", midB.join(""));
  } else if (n === 0 && m > 0) {
    pushSegment(segments, "removed", midA.join(""));
  } else if (m > 0 && n > 0) {
    if ((m + 1) * (n + 1) <= MAX_DP_CELLS) {
      const cols = n + 1;
      const dp = new Int32Array((m + 1) * cols);
      for (let i = m - 1; i >= 0; i -= 1) {
        const rowOffset = i * cols;
        const nextRowOffset = (i + 1) * cols;
        for (let j = n - 1; j >= 0; j -= 1) {
          if (midA[i] === midB[j]) {
            dp[rowOffset + j] = dp[nextRowOffset + (j + 1)] + 1;
          } else {
            const skipA = dp[nextRowOffset + j];
            const skipB = dp[rowOffset + (j + 1)];
            dp[rowOffset + j] = skipA >= skipB ? skipA : skipB;
          }
        }
      }

      let i = 0;
      let j = 0;
      while (i < m && j < n) {
        if (midA[i] === midB[j]) {
          pushSegment(segments, "equal", midA[i]);
          i += 1;
          j += 1;
        } else if (dp[(i + 1) * cols + j] >= dp[i * cols + (j + 1)]) {
          pushSegment(segments, "removed", midA[i]);
          i += 1;
        } else {
          pushSegment(segments, "added", midB[j]);
          j += 1;
        }
      }
      while (i < m) {
        pushSegment(segments, "removed", midA[i]);
        i += 1;
      }
      while (j < n) {
        pushSegment(segments, "added", midB[j]);
        j += 1;
      }
    } else {
      pushSegment(segments, "removed", midA.join(""));
      pushSegment(segments, "added", midB.join(""));
    }
  }

  for (let index = a.length - suffix; index < a.length; index += 1) {
    pushSegment(segments, "equal", a[index]);
  }
  return normalizeEditRuns(segments);
}

export function computeWordDiff(
  original: string,
  revised: string,
): DiffSegment[] {
  if (original === revised) {
    return original ? [{ kind: "equal", text: original }] : [];
  }
  if (!original) {
    return [{ kind: "added", text: revised }];
  }
  if (!revised) {
    return [{ kind: "removed", text: original }];
  }

  const originalTokens = tokenize(original);
  const revisedTokens = tokenize(revised);
  if (
    (originalTokens.length + 1) * (revisedTokens.length + 1) <=
    MAX_DP_CELLS
  ) {
    return diffSequence(originalTokens, revisedTokens);
  }

  // Fallback to line-level diff when huge edited spans exceed token DP budget.
  return diffSequence(
    original.split(/(\n+)/).filter(Boolean),
    revised.split(/(\n+)/).filter(Boolean),
  );
}
