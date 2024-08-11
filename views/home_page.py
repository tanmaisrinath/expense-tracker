import streamlit as st


# Page title
st.markdown(
    "<h1 style='text-align: center;'>Welcome to TickTrack2</h1>",
    unsafe_allow_html=True,
)

# Add a horizontal line
st.markdown("<hr>", unsafe_allow_html=True)

# Add description
st.write(
    """
    Tired of arguing over who paid for what? Our Expense Tracker for Two makes it easy to keep your 
    finances in check with a touch of fun. Record your shared expenses, split costs with a click, 
    and see who owes whom without the drama. It’s like having a personal accountant, but way cooler. 
    Keep track of everything in real-time, stay on top of your spending, and enjoy smooth sailing in 
    your financial adventures together!
    """
)

# Use columns to place paragraphs side by side
col1, col2, col3 = st.columns(3)

with col1:
    st.write(
        """
        Ready to confess your spending sins? Drop your latest splurge, 
        surprise costs, or those relentless bills right here. Click that
        button below and let the expense tracking begin—your wallet 
        might not love it, but it'll definitely thank you later.
        """
    )

with col2:
    st.write(
        """
        Curious where your cash has been sneaking off to? Click here to 
        unveil the details and face the music. It's like your spending's 
        personal highlight reel—minus the glam, but full of reality checks.
        """
    )

with col3:
    st.write(
        """
        Time for the grand tour of your finances! Click here to see your expense 
        dashboard and witness the full spectacle of your spending habits. Spoiler:
        It's more dramatic than you think, and it's all about to unfold!
        """
    )
