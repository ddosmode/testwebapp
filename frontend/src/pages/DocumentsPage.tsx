import PageContainer from "@/widgets/PageContainer";
import Header from "@/widgets/Header";
import { useNavigate } from "react-router-dom";
import { FileText, ArrowRight, Shield } from "lucide-react";
import { useLegalStore } from "@/entities/legalStore";

export default function DocumentsPage() {
  const navigate = useNavigate();
  const acceptedDocuments = useLegalStore((state) => state.acceptedDocuments);

  const documentTypes = [
    {
      id: "terms",
      title: "Terms of Service",
      description: "General terms and conditions for using our platform",
      icon: FileText,
    },
    {
      id: "privacy",
      title: "Privacy Policy",
      description: "How we collect, use, and protect your data",
      icon: Shield,
    },
    {
      id: "delivery",
      title: "Delivery Policy",
      description: "Shipping and delivery information",
      icon: FileText,
    },
    {
      id: "returns",
      title: "Return Policy",
      description: "Returns and refunds policy",
      icon: FileText,
    },
  ];

  return (
    <PageContainer>
      <Header title="Documents" />
      
      <div className="p-4 space-y-4">
        <p className="text-sm text-muted-foreground">
          Review and accept legal documents to continue using the platform
        </p>

        <div className="space-y-3">
          {documentTypes.map((doc) => {
            const isAccepted = !!acceptedDocuments[doc.id];
            return (
              <button
                key={doc.id}
                onClick={() => navigate(`/legal?doc=${doc.id}`)}
                className="w-full p-4 rounded-lg border text-left flex items-center justify-between hover:bg-muted transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-muted flex items-center justify-center">
                    <doc.icon className="h-5 w-5 text-muted-foreground" />
                  </div>
                  <div>
                    <h3 className="font-medium text-sm">{doc.title}</h3>
                    <p className="text-xs text-muted-foreground mt-0.5">
                      {doc.description}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  {isAccepted && (
                    <span className="text-xs text-green-600 font-medium">
                      Accepted
                    </span>
                  )}
                  <ArrowRight className="h-4 w-4 text-muted-foreground" />
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </PageContainer>
  );
}
