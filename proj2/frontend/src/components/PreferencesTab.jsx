import React from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Separator } from './ui/separator';
import { Slider } from './ui/slider';
import { Switch } from './ui/switch';
import { Label } from './ui/label';
import { Input } from './ui/input';

const AVAILABLE_CUISINES = [
  '🍕 Italian', '🍜 Asian', 'Latino', '🌮 Mexican', '🍔 American', '🥗 Mediterranean',
  '🍛 Indian', '🍱 Japanese', 'Chinese', 'Korean', '🥘 Thai', 'Vietnamese', 
  '🧆 Middle Eastern', '🥖 French'
];

const COMMON_ALLERGENS = [
  '🥜 Nuts', '🥛 Dairy', '🍳 Eggs', '🌾 Gluten', '🦐 Shellfish',
  '🐟 Fish', '🍓 Soy', '🌽 Corn', '🥥 Coconut'
];

const DIETARY_RESTRICTIONS = [
  '🌱 Vegetarian', '🥬 Vegan', '🥩 Keto', '🌾 Gluten-Free', '🧂 Low-Sodium',
  '🍯 Paleo', '🥛 Lactose-Free', '🫘 Kosher', '☪️ Halal'
];

export function PreferencesTab({ preferences, onPreferencesChange }) {
  const toggleArrayItem = (array, item) => {
    return array.includes(item)
      ? array.filter(i => i !== item)
      : [...array, item];
  };

  const handleCuisineToggle = (cuisine) => {
    onPreferencesChange({
      ...preferences,
      cuisines: toggleArrayItem(preferences.cuisines, cuisine)
    });
  };

  const handleAllergenToggle = (allergen) => {
    onPreferencesChange({
      ...preferences,
      allergens: toggleArrayItem(preferences.allergens, allergen)
    });
  };

  const handleDietaryToggle = (dietary) => {
    onPreferencesChange({
      ...preferences,
      dietaryRestrictions: toggleArrayItem(preferences.dietaryRestrictions, dietary)
    });
  };

  return (
    <div className="space-y-4 sm:space-y-6">
      {/* Cuisine Preferences */}
      <Card>
        <CardHeader className="p-4 sm:p-6 pb-2 sm:pb-2">
          <CardTitle className="text-lg sm:text-xl">Cuisine Preferences</CardTitle>
          <CardDescription className="text-sm sm:text-base">
            Select the types of food you enjoy most
          </CardDescription>
        </CardHeader>
        <CardContent className="p-4 sm:p-6 pt-0">
          <div className="flex flex-wrap gap-2">
            {AVAILABLE_CUISINES.map((cuisine) => (
              <Badge
                key={cuisine}
                variant={preferences.cuisines.includes(cuisine) ? "default" : "outline"}
                className={`cursor-pointer transition-all hover:scale-105 ${
                  preferences.cuisines.includes(cuisine)
                    ? 'bg-primary hover:bg-primary/90 text-primary-foreground'
                    : 'hover:border-primary hover:text-primary'
                }`}
                onClick={() => handleCuisineToggle(cuisine)}
              >
                {cuisine}
              </Badge>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Allergens & Dietary Restrictions */}
      <div className="grid sm:grid-cols-2 gap-4 sm:gap-6">
        <Card>
          <CardHeader className="p-4 sm:p-6 pb-2 sm:pb-2">
            <CardTitle className="text-lg sm:text-xl">Allergens</CardTitle>
            <CardDescription className="text-sm sm:text-base">
              Foods you need to avoid
            </CardDescription>
          </CardHeader>
          <CardContent className="p-4 sm:p-6 pt-0">
            <div className="flex flex-wrap gap-2">
              {COMMON_ALLERGENS.map((allergen) => (
                <Badge
                  key={allergen}
                  variant={preferences.allergens.includes(allergen) ? "destructive" : "outline"}
                  className="cursor-pointer transition-all hover:scale-105"
                  onClick={() => handleAllergenToggle(allergen)}
                >
                  {allergen}
                </Badge>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="p-4 sm:p-6 pb-2 sm:pb-2">
            <CardTitle className="text-lg sm:text-xl">Dietary Restrictions</CardTitle>
            <CardDescription className="text-sm sm:text-base">
              Your lifestyle choices
            </CardDescription>
          </CardHeader>
          <CardContent className="p-4 sm:p-6 pt-0">
            <div className="flex flex-wrap gap-2">
              {DIETARY_RESTRICTIONS.map((dietary) => (
                <Badge
                  key={dietary}
                  variant={preferences.dietaryRestrictions.includes(dietary) ? "secondary" : "outline"}
                  className={`cursor-pointer transition-all hover:scale-105 ${
                    preferences.dietaryRestrictions.includes(dietary)
                      ? 'bg-accent hover:bg-accent/90'
                      : 'hover:border-accent hover:text-accent-foreground'
                  }`}
                  onClick={() => handleDietaryToggle(dietary)}
                >
                  {dietary}
                </Badge>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Price Range & Distance */}
      <div className="grid sm:grid-cols-2 gap-4 sm:gap-6">
        <Card>
          <CardHeader className="p-4 sm:p-6 pb-2 sm:pb-2">
            <CardTitle className="text-lg sm:text-xl">Price Range</CardTitle>
            <CardDescription className="text-sm sm:text-base">
              How much are you comfortable spending?
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3 sm:space-y-4 p-4 sm:p-6 pt-2">
            <div className="space-y-3 sm:space-y-4">
              <div className="px-3">
                <Slider
                  value={preferences.priceRange}
                  onValueChange={(value) =>
                    onPreferencesChange({
                      ...preferences,
                      priceRange: value
                    })
                  }
                  max={4}
                  min={1}
                  step={1}
                  className="w-full"
                />
              </div>
              <div className="grid grid-cols-4 text-xs sm:text-sm text-muted-foreground text-center">
                <span>$ Budget</span>
                <span>$$ Moderate</span>
                <span>$$$ Upscale</span>
                <span>$$$$ Fine</span>
              </div>
              <div className="text-center">
                <Badge variant="outline">
                  {preferences.priceRange[0] === preferences.priceRange[1]
                    ? '$'.repeat(preferences.priceRange[0])
                    : '$'.repeat(preferences.priceRange[0]) +
                      ' - ' +
                      '$'.repeat(preferences.priceRange[1])}
                </Badge>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="p-4 sm:p-6 pb-2 sm:pb-2">
            <CardTitle className="text-lg sm:text-xl">Maximum Distance</CardTitle>
            <CardDescription className="text-sm sm:text-base">
              How far are you willing to travel?
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3 sm:space-y-4 p-4 sm:p-6 pt-2">
            <div className="space-y-3 sm:space-y-4">
              <div className="px-3">
                <Slider
                  value={[preferences.maxDistance]}
                  onValueChange={(value) =>
                    onPreferencesChange({
                      ...preferences,
                      maxDistance: value[0]
                    })
                  }
                  max={25}
                  min={1}
                  step={1}
                  className="w-full"
                />
              </div>
              <div className="text-center">
                <Badge variant="outline">{preferences.maxDistance} miles</Badge>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Preferences */}
      <Card>
        <CardHeader className="p-4 sm:p-6 pb-2 sm:pb-2">
          <CardTitle className="text-lg sm:text-xl">Quick Preferences</CardTitle>
          <CardDescription className="text-sm sm:text-base">
            Additional preferences to fine-tune your recommendations
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-3 sm:space-y-4 p-4 sm:p-6 pt-2">
          <div className="flex items-center justify-between gap-4">
            <div className="space-y-0.5 sm:space-y-1 flex-1">
              <Label className="text-sm sm:text-base">Prefer Healthy Options 🥗</Label>
              <p className="text-xs sm:text-sm text-muted-foreground">
                Prioritize restaurants with healthy menu options
              </p>
            </div>
            <Switch
              checked={preferences.preferHealthy}
              onCheckedChange={(checked) =>
                onPreferencesChange({
                  ...preferences,
                  preferHealthy: checked
                })
              }
            />
          </div>
          <Separator />
          <div className="flex items-center justify-between gap-4">
            <div className="space-y-0.5 sm:space-y-1 flex-1">
              <Label className="text-sm sm:text-base">Prefer Quick Service ⚡</Label>
              <p className="text-xs sm:text-sm text-muted-foreground">
                Prioritize fast casual and quick service restaurants
              </p>
            </div>
            <Switch
              checked={preferences.preferQuick}
              onCheckedChange={(checked) =>
                onPreferencesChange({
                  ...preferences,
                  preferQuick: checked
                })
              }
            />
          </div>
        </CardContent>
      </Card>

      {/* User Location */}
      <Card>
        <CardHeader className="p-4 sm:p-6 pb-2 sm:pb-2">
          <CardTitle className="text-lg sm:text-xl">Your Location</CardTitle>
          <CardDescription className="text-sm sm:text-base">
            Set your location to see nearby meals and enable pickup
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-3 sm:space-y-4 p-4 sm:p-6 pt-2">
          <div className="space-y-2">
            <Label htmlFor="location">Address</Label>
            <div className="flex space-x-2">
              <Input
                id="location"
                value={preferences.userLocation?.address || ''}
                onChange={(e) =>
                  onPreferencesChange({
                    ...preferences,
                    userLocation: { address: e.target.value, lat: 0, lng: 0 }
                  })
                }
                placeholder="Enter your address or zip code"
              />
            </div>
            <p className="text-xs text-muted-foreground">
              This helps calculate distance to meals and sets your default pickup location
            </p>
          </div>
        </CardContent>
      </Card>

      <div className="flex justify-end px-4 sm:px-0">
        <Button className="bg-primary hover:bg-primary/90 font-sans w-full sm:w-auto">
          Save Preferences
        </Button>
      </div>
    </div>
  );
}
