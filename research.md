# Research: How much noodles/pasta should FoodCalls boil before each rush?

**Place:** FoodCalls (pizza | burger | chowmein), near my college, Prayagraj
**Person:** Nivesh Gupta, owner of FoodCalls
**Visited:** 20 Nov 2026, approx. 20:20 – 21:15

## The problem (5 lines)

1. FoodCalls boils noodles and pasta in advance so that orders go out fast when students rush in after classes.
2. Boiled noodles/pasta only last a few hours; whatever is left at closing has to be thrown away (sauces are fine, they have preservatives).
3. How much to boil is decided by guess every day - the owner said "quantity is not fixed", some days orders go up, some days they drop.
4. Boil too little and the after-class rush waits (only 18 seats, so slow tables mean turned-away customers); boil too much and it goes in the bin.
5. Goal: a small tool that uses the shop's own sales per time slot to suggest how much to boil before each slot.

## Existing solutions and why they don't fit Nivesh ji

### 1. Billing + inventory software (Petpooja)
- What it does: GST billing with stock tracking (barcode scanning, FIFO/FEFO stock, purchase updates, inventory reports).
- Why it doesn't fit: it tracks stock you *buy and sell*, not food you *prepare in advance*. There is nothing for "boiled 10 plates, threw away 3". It only works if every sale goes through its billing, and the price isn't public (contact sales). Nivesh ji runs on cash and a notebook.

### 2. AI food-waste tracking (Winnow)
- What it does: a camera and scale at the bin recognise and weigh what is thrown away. An add-on (Foresight) forecasts how much to cook each service.
- Why it doesn't fit: it's built for hotel and chain kitchens (Hilton, IKEA, Marriott), with a setup fee plus a per-site subscription. Its savings examples assume food spend in lakhs of dollars. A rented 18-seat shop with 4 staff can't justify the hardware, and the forecasting needs the waste data that the hardware collects first.

## Sources I actually read

*(Read with AI assistance on 21 Nov 2026; links checked working that day.)*

1. **Petpooja - Invoice / billing software** - https://www.petpooja.com/invoice
   Petpooja sells its inventory feature inside the billing software (stock tracking, barcode scanning, FIFO/FEFO, purchase updates).
   The page mentions no recipe, wastage or "how much to prepare" feature. It's about stock bought and sold, not food prepared ahead.
   Pricing isn't shown (Basic/Advanced, "contact us"), and it assumes every sale is billed through it. That's the main mismatch for a cash-and-register shop.

2. **Winnow Solutions** - https://www.winnowsolutions.com/solutions and /pricing
   Winnow puts a camera and scale on the kitchen bin. AI identifies each thrown item, logs weight and cost, and gives chefs daily actions.
   Customers claim big cuts in waste (IKEA 54%, Radisson Blu Bremen 60% over two years, by Winnow's own figures), and a Foresight add-on predicts production per service.
   It's priced per site (setup fee + subscription), aimed at hotels and chains. It confirmed that the idea "forecast production from past data" works, but that the tool has to be tiny for Nivesh ji.
