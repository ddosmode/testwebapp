import { create } from "zustand";
import { persist } from "zustand/middleware";

interface LegalStore {
  acceptedDocuments: Record<string, string>;
  acceptDocument: (docId: string, version: string) => void;
  isAccepted: (docId: string, version: string) => boolean;
  getAcceptedVersion: (docId: string) => string | null;
}

export const useLegalStore = create<LegalStore>()(
  persist(
    (set, get) => ({
      acceptedDocuments: {},
      
      acceptDocument: (docId, version) => {
        set((state) => ({
          acceptedDocuments: { ...state.acceptedDocuments, [docId]: version },
        }));
      },
      
      isAccepted: (docId, version) => {
        return get().acceptedDocuments[docId] === version;
      },
      
      getAcceptedVersion: (docId) => {
        return get().acceptedDocuments[docId] || null;
      },
    }),
    {
      name: "legal-documents-storage",
    }
  )
);
