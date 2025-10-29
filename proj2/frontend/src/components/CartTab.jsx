import React from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';

export default function CheckoutTab({ cart, onRemoveFromCart }) {
  if (!cart.length) {
    return (
      <div className="text-center py-12 space-y-4">
        <h3>Your cart is empty</h3>
        <p className="text-muted-foreground">Add meals from the Browse tab to see them here</p>
      </div>
    );
  }

  // calculate total price
  const totalPrice = cart.reduce((sum, meal) => sum + Number(meal.sale_price), 0);

  return (
    <div className="space-y-4 sm:space-y-6">
      <h2 className="text-xl sm:text-2xl">Your Meal Cart</h2>

      <div className="grid gap-4 sm:gap-6">
        {cart.map((meal) => (
          <Card key={meal.id} className="overflow-hidden hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle>{meal.title}</CardTitle>
            </CardHeader>
            <CardContent className="flex justify-between items-center">
              <span>${meal.sale_price}</span>
              <Button
                size="sm"
                variant="destructive-outline"
                className="cursor-pointer mt-3 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg"
                onClick={() => onRemoveFromCart(meal.id)}
              >
                Remove
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="flex justify-end items-center space-x-4 mt-4">
        <span className="font-semibold text-lg">Total: ${totalPrice.toFixed(2)}</span>
        <Button size="sm" variant="primary" className="cursor-pointer bg-[#D9A299] hover:bg-[#d18e82] text-white px-4 py-2 rounded-lg">
          Checkout
        </Button>
      </div>
    </div>
  );
}
