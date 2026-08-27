import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import PageContainer from "@/widgets/PageContainer";
import Header from "@/widgets/Header";
import { api } from "@/lib/api";
import type { City } from "@/lib/api";
import { Button } from "@/shared/ui/button";
import { Check } from "lucide-react";

export default function CitySelectionPage() {
  const navigate = useNavigate();
  const [cities, setCities] = useState<City[]>([]);
  const [selectedCity, setSelectedCity] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadCities() {
      try {
        const res = await api.get("/locations/cities");
        setCities(res.data);
      } catch (error) {
        console.error("Failed to load cities:", error);
      } finally {
        setIsLoading(false);
      }
    }
    loadCities();
  }, []);

  const handleSelectCity = (cityId: string) => {
    setSelectedCity(cityId);
  };

  const handleContinue = () => {
    if (selectedCity) {
      navigate("/checkout/payment");
    }
  };

  return (
    <PageContainer>
      <Header title="Select City" />
      
      <div className="p-4 space-y-4">
        <p className="text-sm text-muted-foreground">
          Select your city for delivery
        </p>

        {isLoading ? (
          <div className="text-center py-12 text-muted-foreground">Loading...</div>
        ) : (
          <div className="space-y-2">
            {cities.map((city) => (
              <button
                key={city.id}
                onClick={() => handleSelectCity(city.id)}
                className={`w-full p-4 rounded-lg border text-left flex items-center justify-between transition-colors ${
                  selectedCity === city.id
                    ? "border-primary bg-primary/5"
                    : "hover:bg-muted"
                }`}
              >
                <span className="font-medium">{city.name}</span>
                {selectedCity === city.id && (
                  <Check className="h-5 w-5 text-primary" />
                )}
              </button>
            ))}
          </div>
        )}

        <div className="flex gap-3 pt-4">
          <Button
            variant="outline"
            className="flex-1"
            onClick={() => navigate(-1)}
          >
            Back
          </Button>
          <Button
            className="flex-1"
            onClick={handleContinue}
            disabled={!selectedCity}
          >
            Continue
          </Button>
        </div>
      </div>
    </PageContainer>
  );
}
