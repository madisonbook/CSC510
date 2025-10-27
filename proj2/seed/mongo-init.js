(function () {
  const DB = globalThis.db.getSiblingDB('myapp');
  const now = new Date();
  const inHours = (h) => new Date(now.getTime() + h * 3600 * 1000);

  function userDoc({ full_name, email, phone, address, city, state, postal, lat, lng, pic, bio, role='user', verified=false }) {
    return {
      _id: new ObjectId(),
      email,
      full_name,
      phone,
      location: {
        address,
        city,
        state,
        postal_code: postal,
        coordinates: { lat, lng }
      },
      bio,
      profile_picture: pic,
      dietary_preferences: {
        vegetarian: false,
        vegan: false,
        gluten_free: false,
        halal: false,
        kosher: false,
        allergens: []
      },
      social_media: { twitter: '', instagram: '', facebook: '', website: '' },
      role,
      status: 'active',
      stats: { meals_posted: 0, meals_sold: 0, swaps_completed: 0, ratings: { count: 0, average: null } },
      verified,
      created_at: now,
      updated_at: now
    };
  }

  function mealDoc({
    ownerId, title, desc, cuisine, mealType, price, servings,
    swap=false, swapPrefs=[], contains=[], mayContain=[],
    ingredients='', nutrition='', pickup='', photos=[]
  }) {
    return {
      title,
      description: desc,
      cuisine_type: cuisine,
      meal_type: mealType,
      photos,
      portion_size: `${servings} servings`,
      available_for_sale: price > 0,
      sale_price: price,
      available_for_swap: swap,
      swap_preferences: swapPrefs,
      allergen_info: { contains, may_contain: mayContain },
      ingredients,
      nutrition_info: nutrition,
      preparation_date: now.toISOString(),
      expires_date: inHours(24).toISOString(),
      pickup_instructions: pickup,
      status: 'available',
      views: 0,
      owner_id: ownerId,
      seller_id: ownerId,
      created_at: now,
      updated_at: now
    };
  }

  const users = [
    userDoc({
      full_name: 'Ava Johnson',
      email: 'ava@example.com',
      phone: '+1-919-555-0141',
      address: '201 Hillsborough St', city: 'Raleigh', state: 'NC', postal: '27603',
      lat: 35.7796, lng: -78.6382,
      pic: 'https://images.unsplash.com/photo-1531123897727-8f129e1688ce?w=512',
      bio: 'Home cook specializing in Italian comfort food.', verified: true
    }),
    userDoc({
      full_name: 'Marcus Lee',
      email: 'marcus@example.com',
      phone: '+1-984-555-0172',
      address: '11 W Jones St', city: 'Raleigh', state: 'NC', postal: '27601',
      lat: 35.7804, lng: -78.6391,
      pic: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=512',
      bio: 'Plant-forward meals with bold flavors.', verified: true
    }),
    userDoc({
      full_name: 'Sofia Ramirez',
      email: 'sofia@example.com',
      phone: '+1-919-555-0198',
      address: '310 S Harrington St', city: 'Raleigh', state: 'NC', postal: '27601',
      lat: 35.7777, lng: -78.6420,
      pic: 'https://images.unsplash.com/photo-1527980965255-d3b416303d12?w=512',
      bio: 'Big-batch meal prep and Mexican staples.', verified: false
    })
  ];

  DB.users.deleteMany({});
  DB.users.insertMany(users);

  const ava = users[0]._id, marcus = users[1]._id, sofia = users[2]._id;

  const meals = [
    mealDoc({
      ownerId: ava,
      title: 'Homemade Lasagna',
      desc: 'Layers of pasta with ricotta, mozzarella, and slow-simmered sauce.',
      cuisine: 'Italian', mealType: 'Dinner', price: 12.5, servings: 4,
      swap: false, contains: ['🥛 Dairy','🌾 Gluten'], mayContain: ['🍳 Eggs'],
      ingredients: 'Lasagna noodles, ricotta, mozzarella, parmesan, tomato sauce, basil',
      nutrition: 'Calories: 520, Protein: 26g, Carbs: 48g, Fat: 24g',
      pickup: '201 Hillsborough St, Raleigh, NC',
      photos: ['https://images.unsplash.com/photo-1604908176997-4316c6235b03?w=960']
    }),
    mealDoc({
      ownerId: marcus,
      title: 'Tofu Veggie Stir Fry',
      desc: 'Crisp veggies and tofu in garlic-ginger sauce. Vegan.',
      cuisine: '🍜 Asian', mealType: 'Lunch', price: 9.0, servings: 3,
      swap: true, swapPrefs: ['Any vegetarian entree','Whole-grain bread'],
      contains: ['🍓 Soy'], mayContain: [],
      ingredients: 'Tofu, broccoli, bell peppers, snap peas, garlic, ginger, soy sauce',
      nutrition: 'Calories: 380, Protein: 22g, Carbs: 45g, Fat: 12g',
      pickup: '11 W Jones St, Raleigh, NC',
      photos: ['https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=960']
    }),
    mealDoc({
      ownerId: sofia,
      title: 'Chicken Tinga Tacos Kit',
      desc: 'Smoky shredded chicken with tortillas and toppings.',
      cuisine: '🌮 Mexican', mealType: 'Dinner', price: 14.0, servings: 5,
      swap: true, swapPrefs: ['Fresh produce','Homemade bread'],
      contains: [], mayContain: ['🌾 Gluten'],
      ingredients: 'Chicken, chipotle, tomatoes, onions, corn tortillas, cilantro, lime',
      nutrition: 'Calories: 450, Protein: 28g, Carbs: 40g, Fat: 16g',
      pickup: '310 S Harrington St, Raleigh, NC',
      photos: ['https://images.unsplash.com/photo-1552332386-f8dd00dc2f85?w=960']
    }),
    mealDoc({
      ownerId: ava,
      title: 'Caprese Salad Pack',
      desc: 'Tomatoes, fresh mozzarella, basil, balsamic glaze.',
      cuisine: '🥗 Mediterranean', mealType: 'Lunch', price: 7.5, servings: 2,
      swap: false, contains: ['🥛 Dairy'], mayContain: [],
      ingredients: 'Tomatoes, mozzarella, basil, olive oil, balsamic glaze',
      nutrition: 'Calories: 280, Protein: 14g, Carbs: 10g, Fat: 20g',
      pickup: '201 Hillsborough St, Raleigh, NC',
      photos: ['https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=960']
    }),
    mealDoc({
      ownerId: marcus,
      title: 'Thai Green Curry (Mild)',
      desc: 'Coconut curry with mixed vegetables and jasmine rice.',
      cuisine: '🥘 Thai', mealType: 'Dinner', price: 11.0, servings: 3,
      swap: false, contains: ['🥥 Coconut'], mayContain: ['🍓 Soy'],
      ingredients: 'Coconut milk, green curry paste, eggplant, bamboo shoots, basil, rice',
      nutrition: 'Calories: 510, Protein: 12g, Carbs: 68g, Fat: 22g',
      pickup: '11 W Jones St, Raleigh, NC',
      photos: ['https://images.unsplash.com/photo-1617191518601-4c8e6cd0cd2b?w=960']
    })
  ];

  DB.meals.deleteMany({});
  DB.meals.insertMany(meals);

  DB.users.updateOne({ _id: ava },    { $set: { 'stats.meals_posted': 2 }, $currentDate: { updated_at: true } });
  DB.users.updateOne({ _id: marcus }, { $set: { 'stats.meals_posted': 2 }, $currentDate: { updated_at: true } });
  DB.users.updateOne({ _id: sofia },  { $set: { 'stats.meals_posted': 1 }, $currentDate: { updated_at: true } });

  print(`Seeded 'myapp': users=${DB.users.countDocuments()}, meals=${DB.meals.countDocuments()}`);
})();
