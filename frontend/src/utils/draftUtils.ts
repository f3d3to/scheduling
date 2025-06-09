const DRAFT_PREFIX = 'planDraft_';

export function saveDraft(draftId: string, data: any) {
  localStorage.setItem(DRAFT_PREFIX + draftId, JSON.stringify(data));
}

export function loadDraft(draftId: string) {
  const data = localStorage.getItem(DRAFT_PREFIX + draftId);
  return data ? JSON.parse(data) : null;
}

export function listDrafts() {
  return Object.keys(localStorage)
    .filter(key => key.startsWith(DRAFT_PREFIX))
    .map(key => ({
      id: key.replace(DRAFT_PREFIX, ''),
      data: JSON.parse(localStorage.getItem(key)!)
    }));
}

export function removeDraft(draftId: string) {
  localStorage.removeItem(DRAFT_PREFIX + draftId);
}
