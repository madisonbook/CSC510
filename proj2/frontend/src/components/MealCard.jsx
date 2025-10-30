import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "./ui/card";
import { Clock, User2, MapPin, Package, Heart } from "lucide-react";
import { Badge } from './ui/badge';
import { Button } from './ui/button';

export default function MealCard({
  meal,
  onAddToCart,
  onRate,
  onReport,
  userRatings,
  renderStars,
  renderPriceLevel,
  setSelectedMeal,
  setReportingMeal,
  setReportDialogOpen,
  onRemoveFromCart,
  showRemoveFromCart
}) 
{

  return (
    // construction of meal card with all specific info
    <Card key={meal.id} className="overflow-hidden hover:shadow-lg transition-shadow">
      <div className="flex flex-col md:flex-row">
        <div className="w-full md:w-64 h-48 md:h-auto relative overflow-hidden">
          <img
            src={meal.photos?.[0]}
            alt={meal.title}
            className="w-full h-full object-cover hover:scale-105 transition-transform duration-500"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/30 via-transparent to-transparent"></div>
          <div className="absolute top-2 right-2 sm:top-3 sm:right-3 flex flex-col gap-2">
            <Badge className="bg-green-500/90 backdrop-blur-sm text-xs">
              <Clock className="w-3 h-3 mr-1" />
            </Badge>
            {meal.available_for_swap && (
              <Badge className="bg-primary/90 backdrop-blur-sm text-xs sm:text-sm">
                🔄 Swap Available
              </Badge>
            )}
          </div>
        </div>

        <div className="flex-1">
          <CardHeader className="p-4 sm:p-6">
            <div className="flex items-start justify-between">
              <div className="space-y-2 sm:space-y-3">
                <CardTitle className="flex items-center space-x-2 text-lg sm:text-xl">
                  <span>{meal.title}</span>
                  {userRatings?.[meal.id] && (
                    <Heart className="w-4 h-4 fill-red-500 text-red-500 shrink-0" />
                  )}
                </CardTitle>
                <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs sm:text-sm text-muted-foreground">
                  <div className="flex items-center space-x-1">
                    <User2 className="w-3 h-3 shrink-0" />
                    <span>{meal.seller_name}</span>
                  </div>
                  <span>{meal.cuisine_type}</span>
                  <div className="flex items-center space-x-1">
                    <span>{renderPriceLevel?.(meal.sale_price)}</span>
                    <span>${meal.sale_price}</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <MapPin className="w-3 h-3 shrink-0" />
                    <span>{meal.distance} mi away</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Package className="w-3 h-3 shrink-0" />
                    <span>{meal.portion_size}</span>
                  </div>
                </div>
                {renderStars?.(meal.average_rating)}
              </div>
            </div>
            <CardDescription className="text-sm sm:text-base">{meal.description}</CardDescription>
          </CardHeader>

          <CardContent className="p-4 sm:p-6 pt-0">
            <div className="space-y-3 sm:space-y-4">
              <div className="flex items-start space-x-2 text-sm bg-muted/50 p-2 rounded-lg">
                <MapPin className="w-4 h-4 shrink-0 mt-0.5 text-muted-foreground" />
                <div>
                  <p className="font-medium">Pickup Location</p>
                  <p className="text-xs text-muted-foreground">{meal.pickup_instructions}</p>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 sm:gap-4">
                <div className="space-y-2">
                  {meal.allergen_info?.contains?.length > 0 && (
                    <div className="flex flex-col sm:flex-row sm:items-center space-y-1 sm:space-y-0 sm:space-x-2">
                      <span className="text-xs text-muted-foreground shrink-0">Contains:</span>
                      <div className="flex flex-wrap gap-1">
                        {meal.allergen_info.contains.map((allergen) => (
                          <Badge key={allergen} variant="destructive" className="text-xs">
                            {allergen}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}

                  {(meal.ingredients || meal.nutritionInfo) && (
                    <div className="space-y-1 pt-2">
                      {meal.ingredients && (
                        <div className="text-xs sm:text-sm">
                          <span className="font-medium">Ingredients: </span>
                          <span className="text-muted-foreground">{meal.ingredients}</span>
                        </div>
                      )}
                      {meal.nutritionInfo && (
                        <div className="text-xs sm:text-sm">
                          <span className="font-medium">Nutrition: </span>
                          <span className="text-muted-foreground">{meal.nutritionInfo}</span>
                        </div>
                      )}
                    </div>
                  )}
                </div>

                <div className="flex flex-col space-y-2 sm:space-y-3">
                  {onAddToCart && (
                    <Button
                      onClick={() => onAddToCart(meal)}
                      className="cursor-pointer mt-3 bg-[#D9A299] hover:bg-[#d18e82] text-white px-4 py-2 rounded-lg"
                    >
                      Add to Cart
                    </Button>
                  )}

                  {showRemoveFromCart && onRemoveFromCart && (
                    <Button
                      size="sm"
                      variant="destructive-outline"
                      className="cursor-pointer mt-3 bg-[#dc3545] hover:bg-red-600 text-white px-4 py-4 rounded-lg"
                      onClick={() => onRemoveFromCart(meal)}
                    >
                      Remove from Cart
                    </Button>
                  )}

                  {onRate && (
                    <Button
                      size="sm"
                      variant="secondary"
                      className="cursor-pointer"
                      onClick={() => setSelectedMeal(meal)}
                    >
                      Rate Meal
                    </Button>
                  )}

                  {onReport && (
                    <Button
                      size="sm"
                      variant="destructive-outline"
                      className="cursor-pointer bg-[#FAF7F3]"
                      onClick={() => {
                        setReportingMeal(meal);
                        setReportDialogOpen(true);
                      }}
                    >
                      Report
                    </Button>
                  )}
                </div>
              </div>
            </div>
          </CardContent>
        </div>
      </div>
    </Card>
  );
}
