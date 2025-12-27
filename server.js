require('dotenv').config();
const express = require('express');
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const cors = require('cors');

const app = express();
app.use(express.static('public'));
app.use(express.json());
app.use(cors());

const DOMAIN = process.env.DOMAIN || 'http://localhost:4242';

app.post('/create-checkout-session', async (req, res) => {
    const { items } = req.body;

    const lineItems = items.map(item => ({
        price_data: {
            currency: 'usd',
            product_data: {
                name: item.name,
                images: [item.image],
            },
            unit_amount: Math.round(item.price * 100), // Stripe expects cents
        },
        quantity: item.quantity,
    }));

    try {
        const session = await stripe.checkout.sessions.create({
            line_items: lineItems,
            mode: 'payment',
            success_url: `${DOMAIN}/index.html?success=true`,
            cancel_url: `${DOMAIN}/index.html?canceled=true`,
        });

        res.json({ url: session.url });
    } catch (error) {
        console.error('Error creating checkout session:', error);
        res.status(500).json({ error: error.message });
    }
});

const PORT = process.env.PORT || 4242;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
