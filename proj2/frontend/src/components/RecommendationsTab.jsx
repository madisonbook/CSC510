/* eslint-disable no-unused-vars */
import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Star, MapPin, Clock, DollarSign, Heart, User2, MessageCircle, Flag, Package } from 'lucide-react';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { Textarea } from './ui/textarea';
import { Label } from './ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from './ui/alert-dialog';

const MOCK_MEALS = [
  {
    id: '1',
    name: 'Homemade Lasagna',
    cookName: 'Maria R.',
    cuisine: '🍕 Italian',
    description: 'Classic Italian lasagna with layers of homemade pasta, rich meat sauce, béchamel, and mozzarella. Made fresh this morning!',
    rating: 4.9,
    price: 15,
    distance: 0.5,
    location: '123 Main St, Downtown',
    postedAt: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    imageUrl: 'https://images.unsplash.com/photo-1573070640082-32bf80e3efe0?...',
    allergens: ['🥛 Dairy', '🌾 Gluten', '🍳 Eggs'],
    dietaryInfo: [],
    tags: ['Comfort Food', 'Family Recipe', 'Freezer-Friendly'],
    isSwapAvailable: true,
    servings: 4,
    ingredients: 'Ground beef, Ricotta cheese, Mozzarella, Lasagna noodles, Tomato sauce, Herbs',
    nutritionInfo: 'Per serving: 450 cal, 25g protein, 40g carbs, 20g fat'
  },
  // ... (include the rest of your meal objects here)
];

export default function RecommendationsTab({ preferences, userRatings, onRateRestaurant, userLocation }) {
  const [selectedMeal, setSelectedMeal] = useState(null);
  const [ratingValue, setRatingValue] = useState(5);
  const [reviewText, setReviewText] = useState('');
  const [reportDialogOpen, setReportDialogOpen] = useState(false);
  const [reportReason, setReportReason] = useState('');
  const [reportDetails, setReportDetails] = useState('');
  const [reportingMeal, setReportingMeal] = useState(null);

  const getTimeRemaining = (postedAt) => {
    const posted = new Date(postedAt);
    const now = new Date();
    const hoursElapsed = (now - posted) / (1000 * 60 * 60);
    const hoursRemaining = Math.max(0, 24 - hoursElapsed);

    if (hoursRemaining === 0) return 'Expired';
    if (hoursRemaining < 1) return `${Math.round(hoursRemaining * 60)} min left`;
    return `${Math.round(hoursRemaining)}h left`;
  };

  const isExpired = (postedAt) => {
    const posted = new Date(postedAt);
    const now = new Date();
    return (now - posted) / (1000 * 60 * 60) >= 24;
  };

  const handleReport = () => {
    if (!reportReason) {
      alert('Please select a reason for reporting');
      return;
    }
    alert(`Report submitted for "${reportingMeal?.name}". We'll review this within 24 hours.`);
    setReportDialogOpen(false);
    setReportReason('');
    setReportDetails('');
    setReportingMeal(null);
  };

  const getRecommendations = () => {
    return MOCK_MEALS
      .filter(meal => {
        if (isExpired(meal.postedAt)) return false;
        const priceLevel = Math.ceil(meal.price / 10);
        if (priceLevel < preferences.priceRange[0] || priceLevel > preferences.priceRange[1]) return false;
        if (meal.distance > preferences.maxDistance) return false;
        if (preferences.cuisines.length > 0 && !preferences.cuisines.includes(meal.cuisine)) return false;
        if (preferences.allergens.some(allergen => meal.allergens.includes(allergen))) return false;
        if (preferences.dietaryRestrictions.length > 0) {
          const hasMatchingDiet = preferences.dietaryRestrictions.some(diet =>
            meal.dietaryInfo.includes(diet)
          );
          if (!hasMatchingDiet) return false;
        }
        return true;
      })
      .map(meal => {
        let score = meal.rating;
        if (preferences.cuisines.includes(meal.cuisine)) score += 0.4;
        preferences.dietaryRestrictions.forEach(diet => {
          if (meal.dietaryInfo.includes(diet)) score += 0.3;
        });
        score -= meal.distance * 0.1;
        return { ...meal, score };
      })
      .sort((a, b) => b.score - a.score);
  };

  const recommendations = getRecommendations();

  const handleRateMeal = () => {
    if (selectedMeal) {
      onRateRestaurant(selectedMeal.id, ratingValue, reviewText);
      setSelectedMeal(null);
      setRatingValue(5);
      setReviewText('');
    }
  };

  const renderStars = (rating, interactive = false, onRatingChange) => (
    <div className="flex items-center space-x-1">
      {[1, 2, 3, 4, 5].map(star => (
        <Star
          key={star}
          className={`w-4 h-4 ${star <= rating ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300'} ${interactive ? 'cursor-pointer hover:text-yellow-400' : ''}`}
          onClick={interactive && onRatingChange ? () => onRatingChange(star) : undefined}
        />
      ))}
      <span className="ml-2 text-sm text-muted-foreground">{rating.toFixed(1)}</span>
    </div>
  );

  if (recommendations.length === 0) {
    return (
      <div className="text-center py-12 space-y-4">
        <div className="text-6xl">😔</div>
        <h3>No meals match your preferences</h3>
        <p className="text-muted-foreground">Try adjusting your preferences or check back later for new meals</p>
      </div>
    );
  }

  return (
    <div className="space-y-4 sm:space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 sm:gap-0">
        <h2 className="text-xl sm:text-2xl">Available Meals Near You</h2>
        <Badge variant="secondary" className="self-start sm:self-auto">{recommendations.length} meals found</Badge>
      </div>

      <div className="grid gap-4 sm:gap-6">
        {recommendations.map(meal => (
          <Card key={meal.id} className="overflow-hidden hover:shadow-lg transition-shadow">
            <div className="flex flex-col md:flex-row">
              <div className="w-full md:w-64 h-48 md:h-auto relative overflow-hidden">
                <img src={meal.imageUrl} alt={meal.name} className="w-full h-full object-cover hover:scale-105 transition-transform duration-500" />
                <div className="absolute inset-0 bg-gradient-to-t from-black/30 via-transparent to-transparent"></div>
                <div className="absolute top-2 right-2 sm:top-3 sm:right-3 flex flex-col gap-2">
                  <Badge className="bg-green-500/90 backdrop-blur-sm text-xs">
                    <Clock className="w-3 h-3 mr-1" />
                    {getTimeRemaining(meal.postedAt)}
                  </Badge>
                  {meal.isSwapAvailable && <Badge className="bg-primary/90 backdrop-blur-sm text-xs sm:text-sm">🔄 Swap Available</Badge>}
                </div>
              </div>

              <div className="flex-1">
                <CardHeader className="p-4 sm:p-6">
                  <div className="flex items-start justify-between">
                    <div className="space-y-2 sm:space-y-3">
                      <CardTitle className="flex items-center space-x-2 text-lg sm:text-xl">
                        <span>{meal.name}</span>
                        {userRatings[meal.id] && <Heart className="w-4 h-4 fill-red-500 text-red-500 shrink-0" />}
                      </CardTitle>
                      <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs sm:text-sm text-muted-foreground">
                        <div className="flex items-center space-x-1"><User2 className="w-3 h-3 shrink-0" /><span>{meal.cookName}</span></div>
                        <span>{meal.cuisine}</span>
                        <div className="flex items-center space-x-1"><DollarSign className="w-3 h-3 shrink-0" /><span>${meal.price}</span></div>
                        <div className="flex items-center space-x-1"><MapPin className="w-3 h-3 shrink-0" /><span>{meal.distance} mi away</span></div>
                        <div className="flex items-center space-x-1"><Package className="w-3 h-3 shrink-0" /><span>{meal.servings} servings</span></div>
                      </div>
                      {renderStars(meal.rating)}
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
                        <p className="text-xs text-muted-foreground">{meal.location}</p>
                      </div>
                    </div>

                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 sm:gap-4">
                      <div className="space-y-2">
                        <div className="flex flex-wrap gap-2">
                          {meal.tags.slice(0, 3).map(tag => <Badge key={tag} variant="outline" className="text-xs">{tag}</Badge>)}
                        </div>

                        {meal.allergens.length > 0 && (
                          <div className="flex flex-col sm:flex-row sm:items-center space-y-1 sm:space-y-0 sm:space-x-2">
                            <span className="text-xs text-muted-foreground shrink-0">Contains:</span>
                            <div className="flex flex-wrap gap-1">
                              {meal.allergens.map(allergen => <Badge key={allergen} variant="destructive" className="text-xs">{allergen}</Badge>)}
                            </div>
                          </div>
                        )}

                        {(meal.ingredients || meal.nutritionInfo) && (
                          <div className="space-y-1 pt-2">
                            {meal.ingredients && <div className="text-xs sm:text-sm"><span className="font-medium">Ingredients: </span><span className="text-muted-foreground">{meal.ingredients}</span></div>}
                            {meal.nutritionInfo && <div className="text-xs sm:text-sm"><span className="font-medium">Nutrition: </span><span className="text-muted-foreground">{meal.nutritionInfo}</span></div>}
                          </div>
                        )}
                      </div>

                      <div className="flex flex-col space-y-2 sm:space-y-3">
                        <Button size="sm" variant="secondary" onClick={() => setSelectedMeal(meal)}>Rate Meal</Button>
                        <Button size="sm" variant="destructive-outline" onClick={() => { setReportingMeal(meal); setReportDialogOpen(true); }}>Report</Button>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {selectedMeal && (
        <Dialog open={!!selectedMeal} onOpenChange={(open) => { if (!open) setSelectedMeal(null); }}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Rate {selectedMeal.name}</DialogTitle>
              <DialogDescription>Provide a rating and review for this meal</DialogDescription>
            </DialogHeader>

            <div className="space-y-4">
              <div>
                <Label>Rating</Label>
                {renderStars(ratingValue, true, setRatingValue)}
              </div>

              <div>
                <Label>Review</Label>
                <Textarea value={reviewText} onChange={(e) => setReviewText(e.target.value)} placeholder="Write your review..." />
              </div>

              <div className="flex justify-end gap-2">
                <Button variant="secondary" onClick={() => setSelectedMeal(null)}>Cancel</Button>
                <Button onClick={handleRateMeal}>Submit</Button>
              </div>
            </div>
          </DialogContent>
        </Dialog>
      )}

      <AlertDialog open={reportDialogOpen} onOpenChange={setReportDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Report {reportingMeal?.name}</AlertDialogTitle>
            <AlertDialogDescription>Please select a reason and provide any additional details.</AlertDialogDescription>
          </AlertDialogHeader>

          <div className="space-y-4">
            <div>
              <Label>Reason</Label>
              <Select value={reportReason} onValueChange={setReportReason}>
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Select a reason" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Inappropriate Content">Inappropriate Content</SelectItem>
                  <SelectItem value="Spam">Spam</SelectItem>
                  <SelectItem value="Incorrect Information">Incorrect Information</SelectItem>
                  <SelectItem value="Other">Other</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label>Details</Label>
              <Textarea value={reportDetails} onChange={(e) => setReportDetails(e.target.value)} placeholder="Additional details (optional)" />
            </div>

            <AlertDialogFooter className="flex justify-end gap-2">
              <AlertDialogCancel>Cancel</AlertDialogCancel>
              <AlertDialogAction onClick={handleReport}>Submit Report</AlertDialogAction>
            </AlertDialogFooter>
          </div>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}
