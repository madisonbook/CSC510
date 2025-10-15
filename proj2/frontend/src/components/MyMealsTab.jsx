import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Label } from './ui/label';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Switch } from './ui/switch';
import { Separator } from './ui/separator';
import { ScrollArea } from './ui/scroll-area';
import { Plus, MapPin, Clock, DollarSign, Trash2, Package } from 'lucide-react';


const COMMON_ALLERGENS = [
  '🥜 Nuts', '🥛 Dairy', '🍳 Eggs', '🌾 Gluten', '🦐 Shellfish',
  '🐟 Fish', '🍓 Soy', '🌽 Corn', '🥥 Coconut'
];

const DIETARY_INFO = [
  '🌱 Vegetarian', '🥬 Vegan', '🥩 Keto', '🌾 Gluten-Free', '🧂 Low-Sodium',
  '🍯 Paleo', '🥛 Lactose-Free', '🫘 Kosher', '🫘 Halal'
];

const AVAILABLE_CUISINES = [
  '🍕 Italian', '🍜 Asian', '🌮 Mexican', '🍔 American', '🥗 Mediterranean',
  '🍛 Indian', '🍱 Japanese', '🥘 Thai', '🧆 Middle Eastern', '🥖 French'
];

export default function MyMealsTab({ meals, onAddMeal, onDeleteMeal, userLocation }) {
  const [isAddDialogOpen, setIsAddDialogOpen] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    cuisine: '',
    price: '',
    servings: '',
    allergens: [],
    dietaryInfo: [],
    isSwapAvailable: false,
    ingredients: '',
    nutritionInfo: '',
    pickupAddress: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!userLocation && !formData.pickupAddress) {
      alert('Please add your location in Preferences or enter a pickup address');
      return;
    }

    onAddMeal({
      ...formData,
      price: parseFloat(formData.price) || 0,
      servings: parseInt(formData.servings) || 1,
      location: formData.pickupAddress || userLocation?.address || 'Location not specified',
      imageUrl: 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800',
      tags: []
    });

    // Reset form
    setFormData({
      name: '',
      description: '',
      cuisine: '',
      price: '',
      servings: '',
      allergens: [],
      dietaryInfo: [],
      isSwapAvailable: false,
      ingredients: '',
      nutritionInfo: '',
      pickupAddress: ''
    });
    setIsAddDialogOpen(false);
  };

  const toggleArrayItem = (array, item) => {
    return array.includes(item)
      ? array.filter(i => i !== item)
      : [...array, item];
  };

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
    const hoursElapsed = (now - posted) / (1000 * 60 * 60);
    return hoursElapsed >= 24;
  };

  const activeMeals = meals.filter(meal => !isExpired(meal.postedAt));

  return (
    <div className="space-y-4 sm:space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <h2 className="text-xl sm:text-2xl mb-2">Your Meals</h2>
          <p className="text-sm sm:text-base text-muted-foreground">
            Share your homemade creations with the community
          </p>
        </div>
        <Dialog open={isAddDialogOpen} onOpenChange={setIsAddDialogOpen}>
          <DialogTrigger asChild>
            <Button className="bg-primary hover:bg-primary/90 w-full sm:w-auto">
              <Plus className="w-4 h-4 mr-2" />
              Add Meal
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-2xl h-[90vh] sm:h-auto sm:max-h-[90vh] p-0 gap-0 flex flex-col">
            <div className="px-4 sm:px-6 py-4 border-b flex-shrink-0">
              <DialogHeader>
                <DialogTitle className="text-lg sm:text-xl">Add New Meal</DialogTitle>
                <DialogDescription className="text-sm sm:text-base">
                  Share your homemade meal with the community. Meals are available for 24 hours.
                </DialogDescription>
              </DialogHeader>
            </div>
            <ScrollArea className="flex-1">
              <form onSubmit={handleSubmit} className="flex flex-col">
                <div className="px-4 sm:px-6 py-4 space-y-4 sm:space-y-5">
                  {/* Meal Name + Cuisine */}
                  <div className="grid sm:grid-cols-2 gap-3 sm:gap-4">
                    <div className="space-y-1.5 sm:space-y-2">
                      <Label htmlFor="name" className="text-sm">Meal Name *</Label>
                      <Input
                        id="name"
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                        placeholder="e.g., Homemade Lasagna"
                        required
                        className="h-9 sm:h-10"
                      />
                    </div>
                    <div className="space-y-1.5 sm:space-y-2">
                      <Label htmlFor="cuisine" className="text-sm">Cuisine *</Label>
                      <Select
                        value={formData.cuisine}
                        onValueChange={(value) => setFormData({ ...formData, cuisine: value })}
                        required
                      >
                        <SelectTrigger className="h-9 sm:h-10">
                          <SelectValue placeholder="Select cuisine" />
                        </SelectTrigger>
                        <SelectContent>
                          {AVAILABLE_CUISINES.map((cuisine) => (
                            <SelectItem key={cuisine} value={cuisine}>
                              {cuisine}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  {/* Description */}
                  <div className="space-y-1.5 sm:space-y-2">
                    <Label htmlFor="description" className="text-sm">Description *</Label>
                    <Textarea
                      id="description"
                      value={formData.description}
                      onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                      placeholder="Describe your meal..."
                      rows={3}
                      required
                      className="resize-none text-sm"
                    />
                  </div>

                  {/* Price + Servings */}
                  <div className="grid sm:grid-cols-2 gap-3 sm:gap-4">
                    <div className="space-y-1.5 sm:space-y-2">
                      <Label htmlFor="price" className="text-sm">Price ($) *</Label>
                      <Input
                        id="price"
                        type="number"
                        step="0.01"
                        value={formData.price}
                        onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                        placeholder="15.00"
                        required
                        className="h-9 sm:h-10"
                      />
                    </div>
                    <div className="space-y-1.5 sm:space-y-2">
                      <Label htmlFor="servings" className="text-sm">Servings *</Label>
                      <Input
                        id="servings"
                        type="number"
                        value={formData.servings}
                        onChange={(e) => setFormData({ ...formData, servings: e.target.value })}
                        placeholder="4"
                        required
                        className="h-9 sm:h-10"
                      />
                    </div>
                  </div>

                  {/* Pickup Address */}
                  <div className="space-y-1.5 sm:space-y-2">
                    <Label htmlFor="pickupAddress" className="text-sm">Pickup Location</Label>
                    <Input
                      id="pickupAddress"
                      value={formData.pickupAddress}
                      onChange={(e) => setFormData({ ...formData, pickupAddress: e.target.value })}
                      placeholder={userLocation?.address || "Enter pickup address"}
                      className="h-9 sm:h-10"
                    />
                    {!userLocation && (
                      <p className="text-xs text-muted-foreground mt-1">
                        Or set your default location in Preferences
                      </p>
                    )}
                  </div>

                  <Separator className="my-3 sm:my-4" />

                  {/* Allergens */}
                  <div className="space-y-1.5 sm:space-y-2">
                    <Label className="text-sm">Allergens</Label>
                    <div className="flex flex-wrap gap-1.5 sm:gap-2">
                      {COMMON_ALLERGENS.map((allergen) => (
                        <Badge
                          key={allergen}
                          variant={formData.allergens.includes(allergen) ? "destructive" : "outline"}
                          className="cursor-pointer text-xs hover:scale-105 transition-transform"
                          onClick={() =>
                            setFormData({
                              ...formData,
                              allergens: toggleArrayItem(formData.allergens, allergen)
                            })
                          }
                        >
                          {allergen}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  {/* Dietary Info */}
                  <div className="space-y-1.5 sm:space-y-2">
                    <Label className="text-sm">Dietary Information</Label>
                    <div className="flex flex-wrap gap-1.5 sm:gap-2">
                      {DIETARY_INFO.map((info) => (
                        <Badge
                          key={info}
                          variant={formData.dietaryInfo.includes(info) ? "secondary" : "outline"}
                          className="cursor-pointer text-xs hover:scale-105 transition-transform"
                          onClick={() =>
                            setFormData({
                              ...formData,
                              dietaryInfo: toggleArrayItem(formData.dietaryInfo, info)
                            })
                          }
                        >
                          {info}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  <Separator className="my-3 sm:my-4" />

                  {/* Ingredients */}
                  <div className="space-y-1.5 sm:space-y-2">
                    <Label htmlFor="ingredients" className="text-sm">Ingredients (Optional)</Label>
                    <Textarea
                      id="ingredients"
                      value={formData.ingredients}
                      onChange={(e) => setFormData({ ...formData, ingredients: e.target.value })}
                      placeholder="List main ingredients (e.g., Tomatoes, Mozzarella, Basil, Olive Oil)"
                      rows={2}
                      className="resize-none text-sm"
                    />
                  </div>

                  {/* Nutrition Info */}
                  <div className="space-y-1.5 sm:space-y-2">
                    <Label htmlFor="nutritionInfo" className="text-sm">Nutrition Info (Optional)</Label>
                    <Textarea
                      id="nutritionInfo"
                      value={formData.nutritionInfo}
                      onChange={(e) => setFormData({ ...formData, nutritionInfo: e.target.value })}
                      placeholder="e.g., Calories: 450, Protein: 25g, Carbs: 40g, Fat: 15g"
                      rows={2}
                      className="resize-none text-sm"
                    />
                  </div>

                  {/* Swap Available */}
                  <div className="flex items-center justify-between p-3 rounded-lg border bg-muted/30">
                    <div className="space-y-0.5 flex-1">
                      <Label className="text-sm font-medium">Available for Swap</Label>
                      <p className="text-xs text-muted-foreground">
                        Allow meal swaps with other cooks
                      </p>
                    </div>
                    <Switch
                      checked={formData.isSwapAvailable}
                      onCheckedChange={(checked) =>
                        setFormData({ ...formData, isSwapAvailable: checked })
                      }
                    />
                  </div>
                </div>

                <div className="border-t px-4 sm:px-6 py-3 sm:py-4 bg-muted/30 mt-4">
                  <div className="flex flex-col-reverse sm:flex-row justify-end gap-2 sm:gap-3">
                    <Button
                      type="button"
                      variant="outline"
                      onClick={() => setIsAddDialogOpen(false)}
                      className="w-full sm:w-auto"
                    >
                      Cancel
                    </Button>
                    <Button
                      type="submit"
                      className="bg-primary hover:bg-primary/90 w-full sm:w-auto"
                    >
                      Add Meal
                    </Button>
                  </div>
                </div>
              </form>
            </ScrollArea>
          </DialogContent>
        </Dialog>
      </div>

      {activeMeals.length === 0 ? (
        <div className="text-center py-12 space-y-4">
          <div className="text-6xl">🍳</div>
          <h3 className="text-xl">No meals yet</h3>
          <p className="text-muted-foreground max-w-md mx-auto">
            Start sharing your homemade creations! Click "Add Meal" to get started.
          </p>
        </div>
      ) : (
        <div className="grid gap-4 sm:gap-6">
          {activeMeals.map((meal) => (
            <Card key={meal.id} className="overflow-hidden">
              <div className="flex flex-col md:flex-row">
                <div className="w-full md:w-48 h-32 md:h-auto relative overflow-hidden">
                  <img
                    src={meal.imageUrl}
                    alt={meal.name}
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute top-2 right-2">
                    <Badge className="bg-green-500/90 backdrop-blur-sm text-xs">
                      <Clock className="w-3 h-3 mr-1" />
                      {getTimeRemaining(meal.postedAt)}
                    </Badge>
                  </div>
                </div>
                <div className="flex-1">
                  <CardHeader className="p-4 sm:p-6">
                    <div className="flex items-start justify-between">
                      <div className="flex-1 space-y-2">
                        <CardTitle className="text-lg sm:text-xl">{meal.name}</CardTitle>
                        <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs sm:text-sm text-muted-foreground">
                          <span>{meal.cuisine}</span>
                          <div className="flex items-center space-x-1">
                            <DollarSign className="w-3 h-3" />
                            <span>${meal.price}</span>
                          </div>
                          <div className="flex items-center space-x-1">
                            <Package className="w-3 h-3" />
                            <span>{meal.servings} servings</span>
                          </div>
                          <div className="flex items-center space-x-1">
                            <MapPin className="w-3 h-3" />
                            <span className="truncate max-w-[200px]">{meal.location}</span>
                          </div>
                        </div>
                      </div>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => onDeleteMeal(meal.id)}
                        className="text-destructive hover:text-destructive hover:bg-destructive/10"
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                    <CardDescription className="text-sm">{meal.description}</CardDescription>
                  </CardHeader>
                  <CardContent className="p-4 sm:p-6 pt-0">
                    <div className="space-y-3">
                      <div className="flex flex-wrap gap-2">
                        {meal.allergens?.length > 0 && meal.allergens.map((allergen) => (
                          <Badge key={allergen} variant="destructive" className="text-xs">
                            {allergen}
                          </Badge>
                        ))}
                        {meal.dietaryInfo?.length > 0 && meal.dietaryInfo.map((info) => (
                          <Badge key={info} className="text-xs bg-accent">
                            {info}
                          </Badge>
                        ))}
                        {meal.isSwapAvailable && (
                          <Badge className="text-xs bg-primary">🔄 Swap Available</Badge>
                        )}
                      </div>

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
                  </CardContent>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
