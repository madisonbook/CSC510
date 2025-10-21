/* eslint-disable no-unused-vars */
import { useEffect, useState } from 'react';
import { Button } from './ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Avatar, AvatarFallback } from './ui/avatar';
import { Badge } from './ui/badge';
import { LogOut, Settings, User, Star } from 'lucide-react';
import { PreferencesTab } from './PreferencesTab';
import RecommendationsTab from './RecommendationsTab';
import MyMealsTab from './MyMealsTab';


export default function Dashboard({ userId, onLogout }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(null);
  const [myMeals, setMyMeals] = useState([]);
  const backendURL = "http://localhost:8000";

  // fetch current user info
  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await fetch(`${backendURL}/api/users/me`, {
          method: "POST",
          headers: { "Content-Type": "application/json"},
          body: JSON.stringify({ id:userId })
        });
        if (!res.ok) throw new Error("Failed to fetch user data");
        const data = await res.json();
        setUser(data);

      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    if (userId) fetchUser();
  }, [userId]);

  // fetch user's meals
  useEffect(() => {
    const fetchMeals = async () => {
      try {
        const res = await fetch(`${backendURL}/api/meals/my/listings`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ seller_id: userId })
        });
        if (!res.ok) throw new Error("Failed to fetch meals");
        const data = await res.json();
        setMyMeals(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    if (userId) fetchMeals();
  }, [userId]);


  
  const [preferences, setPreferences] = useState({
    cuisines: [], // Empty by default - show all cuisines
    allergens: [],
    dietaryRestrictions: [],
    priceRange: [1, 4], // Show all price ranges by default
    maxDistance: 25, // Maximum distance
    preferHealthy: false,
    preferQuick: true,
    userLocation: null // Will store { address: string, lat: number, lng: number }
  });

  const [userRatings, setUserRatings] = useState({});

  const handleRateRestaurant = (restaurantId, rating, review) => {
    setUserRatings(prev => ({
      ...prev,
      [restaurantId]: { rating, review }
    }));
  };

  const handleAddMeal = (meal) => {
    const newMeal = {
      ...meal,
      id: Date.now().toString(),
      cookName: userId.split('@')[0],
      rating: 0,
      postedAt: new Date().toISOString()
    };
    setMyMeals(prev => [...prev, newMeal]);
  };

  const handleDeleteMeal = (mealId) => {
    setMyMeals(prev => prev.filter(m => m.id !== mealId));
  };

  const getTotalRatings = () => Object.keys(userRatings).length;

  const getAverageRating = () => {
    const ratings = Object.values(userRatings);
    if (ratings.length === 0) return 0;
    const sum = ratings.reduce((acc, curr) => acc + curr.rating, 0);
    return sum / ratings.length;
  };

  if (loading) return <p>Loading user data...</p>;

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-secondary/50 to-accent/30">
      {/* Header */}
      <header className="bg-white/90 backdrop-blur-sm border-b border-primary/10 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4 sm:py-5">
          <div className="flex items-center justify-between">
            {/* Logo and title */}
            <div className="flex items-center space-x-2 sm:space-x-4">
              <div className="w-8 h-8 sm:w-10 sm:h-10 bg-primary rounded-2xl flex items-center justify-center">
                <span className="text-primary-foreground text-base sm:text-lg">🍽️</span>
              </div>
              <h1 className="text-lg sm:text-2xl font-serif font-semibold text-primary">Taste Buddiez</h1>
            </div>

            {/* User section */}
            <div className="flex items-center space-x-2 sm:space-x-4">
              <div className="hidden md:flex items-center space-x-4 lg:space-x-6 text-sm">
                <div className="flex items-center space-x-2">
                  <Star className="w-4 h-4 text-yellow-500" />
                  <span>{getTotalRatings()} ratings</span>
                </div>
                {getTotalRatings() > 0 && (
                  <Badge variant="secondary">
                    Avg: {getAverageRating().toFixed(1)}⭐
                  </Badge>
                )}
              </div>

              <div className="flex items-center space-x-1 sm:space-x-3">
                <Avatar className="w-8 h-8 sm:w-10 sm:h-10">
                  <AvatarFallback>
                    <User className="w-3 h-3 sm:w-4 sm:h-4" />
                  </AvatarFallback>
                </Avatar>
                <div className="hidden md:block">
                  <p className="text-sm">{userId}</p>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={onLogout}
                  className="h-8 w-8 sm:h-9 sm:w-9"
                >
                  <LogOut className="w-3 h-3 sm:w-4 sm:h-4" />
                </Button>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-6 sm:py-8">
        <div className="mb-8 sm:mb-12">
          <h1 className="text-3xl sm:text-4xl md:text-5xl mb-3 sm:mb-4 tracking-tight font-serif font-semibold text-primary">
            Welcome back, {user?.full_name ? user.full_name.split(' ')[0] : "User"}!!
          </h1>
          <p className="text-base sm:text-lg text-muted-foreground font-sans">
            Ready to discover delicious homemade meals or share your own creations?
          </p>
        </div>

        <Tabs defaultValue="browse" className="space-y-4 sm:space-y-6">
          <TabsList className="grid w-full max-w-2xl grid-cols-4 h-auto">
            <TabsTrigger
              value="browse"
              className="flex flex-col sm:flex-row items-center space-x-0 sm:space-x-2 space-y-1 sm:space-y-0 text-xs sm:text-sm py-2 sm:py-2.5 transition-all duration-200"
            >
              <span className="text-base sm:text-lg">🍽️</span>
              <span className="hidden sm:inline">Browse Meals</span>
              <span className="sm:hidden">Browse</span>
            </TabsTrigger>

            <TabsTrigger
              value="my-meals"
              className="flex flex-col sm:flex-row items-center space-x-0 sm:space-x-2 space-y-1 sm:space-y-0 text-xs sm:text-sm py-2 sm:py-2.5 transition-all duration-200"
            >
              <span className="text-base sm:text-lg">📋</span>
              <span className="hidden sm:inline">My Meals</span>
              <span className="sm:hidden">Meals</span>
            </TabsTrigger>

            <TabsTrigger
              value="badges"
              className="flex flex-col sm:flex-row items-center space-x-0 sm:space-x-2 space-y-1 sm:space-y-0 text-xs sm:text-sm py-2 sm:py-2.5 transition-all duration-200"
            >
              <span className="text-base sm:text-lg">🏆</span>
              <span>Badges</span>
            </TabsTrigger>

            <TabsTrigger
              value="preferences"
              className="flex flex-col sm:flex-row items-center space-x-0 sm:space-x-2 space-y-1 sm:space-y-0 text-xs sm:text-sm py-2 sm:py-2.5 transition-all duration-200"
            >
              <span className="text-base sm:text-lg">⚙️</span>
              <span className="hidden lg:inline">Preferences</span>
              <span className="lg:hidden">Settings</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="browse">
            <RecommendationsTab
              preferences={preferences}
              userRatings={userRatings}
              onRateRestaurant={handleRateRestaurant}
              userLocation={preferences.userLocation}
            />
          </TabsContent>

          <TabsContent value="my-meals">
            <MyMealsTab
              meals={myMeals}
              onAddMeal={handleAddMeal}
              onDeleteMeal={handleDeleteMeal}
              userLocation={preferences.userLocation}
            />
          </TabsContent>

          <TabsContent value="badges">
            <div className="space-y-4 sm:space-y-6">
              <div>
                <h2 className="text-xl sm:text-2xl mb-2">Your Badges</h2>
                <p className="text-sm sm:text-base text-muted-foreground">
                  Earn badges for great reviews, successful swaps, and being an active community member
                </p>
              </div>
              <div className="text-center py-12 space-y-4">
                <div className="text-6xl">🏆</div>
                <h3 className="text-xl">No badges yet</h3>
                <p className="text-muted-foreground max-w-md mx-auto">
                  Start rating meals and participating in swaps to earn your first badge!
                </p>
                <div className="pt-4">
                  <p className="text-sm text-muted-foreground italic">
                    Feature coming soon: View and showcase your earned badges
                  </p>
                </div>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="preferences">
            <PreferencesTab
              preferences={preferences}
              onPreferencesChange={setPreferences}
            />
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}
