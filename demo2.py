from synthora.agents import VanillaAgent
from whatsapp import WhatsApp
from prompts import ORDER_PROMPT, PRODUCT_PROMPT, MAIN_PROMPT, GUARD_PROMPT
from dotenv import load_dotenv
from tools import OrderToolkits, ProductToolkits


if __name__ == '__main__':
    load_dotenv()
    app = WhatsApp()
    app.auto_reply(["Hello", "Hi"], "Hi! I am Synthora, your assistant for food product and order inquiries.")
    app.auto_reply(["Bye", "Goodbye"], "Goodbye! Have a great day!", threshold=0.7)
    app.auto_reply(["Thank you", "Thanks"], "You're welcome!", threshold=0.6)

   
    app.auto_reply(["delivery time", "delivery date", "How long will it take to deliver"], "Your order will be delivered within 3-5 business days.", threshold=0.8)
    app.auto_reply(["urgent delivery", "express shipping"], "We offer express delivery for an additional fee. Would you like to upgrade your shipping?")

    
    app.auto_reply(["ingredients", "what's in this product", "nutritional value"], "You can find ingredient details and nutritional values on our product page.")
    app.auto_reply(["allergy", "does this contain nuts", "gluten-free"], "Please check the allergy information on the packaging or our website.")
    app.auto_reply(["organic", "is this product organic"], "Yes, our products are certified organic.")

   
    app.auto_reply(["return policy", "can I return", "refund"], "You can return unopened items within 14 days. Please visit our return policy page for details.")
    app.auto_reply(["damaged product", "received wrong item"], "We apologize for the inconvenience. Please contact our support team for assistance.")

    
    app.auto_reply(["expiration date", "shelf life"], "Our products come with an expiration date printed on the packaging.")
    app.auto_reply(["food safety", "is this product safe"], "Yes, we follow strict food safety regulations to ensure high quality.")



    order_agent = VanillaAgent.default(
        ORDER_PROMPT,
        "Order Agent",
        tools=[OrderToolkits.sync_tools]
    )

    product_agent = VanillaAgent.default(
        PRODUCT_PROMPT,
        "Product Agent",
        tools=[ProductToolkits.sync_tools]
    )

    guard_agent = VanillaAgent.default(
        GUARD_PROMPT,
        "Guard Agent",
    )

    main_agent = VanillaAgent.default(
        MAIN_PROMPT,
        "Main Agent",
        tools=[order_agent, product_agent, app.send_messsage]
    )

    app.set_guard_agent(guard_agent)
    app.set_main_agent(main_agent)

    main_agent.run()

