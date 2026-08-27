import { useState, useEffect } from "react";
import PageContainer from "@/widgets/PageContainer";
import Header from "@/widgets/Header";
import { api } from "@/lib/api";
import type { LegalDocument } from "@/lib/api";
import { useLegalStore } from "@/entities/legalStore";
import { Button } from "@/shared/ui/button";
import { FileText, Shield, CheckCircle2 } from "lucide-react";

export default function LegalAcceptancePage() {
  const [documents, setDocuments] = useState<LegalDocument[]>([]);
  const [acceptedIds, setAcceptedIds] = useState<Set<string>>(new Set());
  const [isLoading, setIsLoading] = useState(true);
  const acceptDocument = useLegalStore((state) => state.acceptDocument);

  useEffect(() => {
    async function loadDocuments() {
      try {
        const res = await api.get("/legal/documents");
        setDocuments(res.data);
      } catch (error) {
        console.error("Failed to load documents:", error);
      } finally {
        setIsLoading(false);
      }
    }
    loadDocuments();
  }, []);

  const handleAccept = async (doc: LegalDocument) => {
    try {
      await api.post(`/legal/documents/${doc.id}/accept`, {
        version: doc.version,
      });
      acceptDocument(doc.id, doc.version);
      setAcceptedIds((prev) => new Set(prev).add(doc.id));
    } catch (error) {
      console.error("Failed to accept document:", error);
    }
  };

  const allAccepted = documents.length > 0 && 
    documents.every((doc) => acceptedIds.has(doc.id));

  if (isLoading) {
    return (
      <PageContainer>
        <Header title="Legal Documents" />
        <div className="p-4 text-center text-muted-foreground">Loading...</div>
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <Header title="Legal Documents" />
      
      <div className="p-4 space-y-4">
        <div className="flex items-center gap-3 p-4 bg-blue-50 dark:bg-blue-950 rounded-lg border border-blue-200 dark:border-blue-800">
          <Shield className="h-5 w-5 text-blue-600 dark:text-blue-400" />
          <div>
            <p className="text-sm font-medium text-blue-900 dark:text-blue-100">
              Required Documents
            </p>
            <p className="text-xs text-blue-700 dark:text-blue-300">
              Please review and accept all documents to continue
            </p>
          </div>
        </div>

        <div className="space-y-3">
          {documents.map((doc) => {
            const isAccepted = acceptedIds.has(doc.id);
            return (
              <div
                key={doc.id}
                className="border rounded-lg p-4 space-y-3"
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-3">
                    <FileText className="h-5 w-5 text-muted-foreground mt-0.5" />
                    <div>
                      <h3 className="font-medium text-sm">{doc.title}</h3>
                      <p className="text-xs text-muted-foreground mt-1">
                        Version {doc.version}
                      </p>
                    </div>
                  </div>
                  {isAccepted && (
                    <CheckCircle2 className="h-5 w-5 text-green-500" />
                  )}
                </div>

                <div className="bg-muted/50 rounded p-3 max-h-40 overflow-y-auto">
                  <p className="text-xs text-muted-foreground leading-relaxed whitespace-pre-wrap">
                    {doc.content}
                  </p>
                </div>

                <Button
                  onClick={() => handleAccept(doc)}
                  disabled={isAccepted}
                  className="w-full"
                  variant={isAccepted ? "outline" : "default"}
                >
                  {isAccepted ? "Accepted" : "Accept Document"}
                </Button>
              </div>
            );
          })}
        </div>

        {allAccepted && (
          <div className="p-4 bg-green-50 dark:bg-green-950 rounded-lg border border-green-200 dark:border-green-800">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-5 w-5 text-green-600 dark:text-green-400" />
              <p className="text-sm font-medium text-green-900 dark:text-green-100">
                All documents accepted
              </p>
            </div>
          </div>
        )}
      </div>
    </PageContainer>
  );
}
